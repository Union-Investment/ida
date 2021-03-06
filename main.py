import uvicorn
from starlette.responses import RedirectResponse
from fastapi import FastAPI, HTTPException, File, UploadFile
from typing import Optional, List
from csv import reader


### gloabls
app = FastAPI()
indices = []

@app.get("/")
async def redirect():
  response = RedirectResponse(url='/docs')
  return response

@app.get("/getdata/{date}")
async def read_item(date: str, index: str = "DAX", show_all_indices: Optional[bool] = False):
  result = {"date": date}

  if date not in fake_items_db:
        raise HTTPException(status_code=404, detail="Date not found")

  elif show_all_indices:
    for i in indices:
      result.update({i: fake_items_db[date][i]})

  else:
    result.update({index: fake_items_db[date][index]})

  return result



@app.post("/uploadfile/")
async def create_upload_files(file: UploadFile = File(...)):
  content = await file.read()

  # add the entries of the uploaded file to fake_items_db
  # data structure of fake_items_db:
  # {"09091990": {"DAX": "1232456", "SP500:" "9238748"}, "08081990":{"DAX": "2345646", "SP500:" "2324432"}, ..}





def add_entries_to_dict(data):
  """
  Adds the entries to the global fake_items_db dictionairy.
  Only available during server runtime.

  Args:
      data (list(list)): [["Date", "DAX", "SP500"], ["30112021", "132345", "762190"], ..]
  """
  for line_no, line in enumerate(data, 0):
    if (line_no == 0):
      new_indices = line[1:]
      for index in new_indices:
        indices.append(index) if index not in indices else indices
        #todo: check order of line of line_no == 0 and indices
    else:
      fake_items_db.update({line[0]: {}})
      for index_no, index in enumerate(indices, 1):
        fake_items_db[line[0]].update({index: line[index_no + 0]})


def initialize_dict(fake_items_db, filename):
  """
  Initializes the fake_items_db dictionairy

  Args:
      fake_items_db (dict): initial empty dictionairy
      filename (string): path to inital file

  Returns:
      dict(dict): {"09091990": {"DAX": "1232456", "SP500:" "9238748"}, "08081990":{"DAX": "2345646", "SP500:" "2324432"} ..}
  """
  file = open('./' + filename, encoding='UTF8')
  csv_reader = reader(file)
  add_entries_to_dict(csv_reader)
  file.close()

  return fake_items_db


fake_items_db = dict()
fake_items_db = initialize_dict(fake_items_db=fake_items_db, filename="daxsp.csv")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
