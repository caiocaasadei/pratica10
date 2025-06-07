
rotasEventoPost = [
    {
        "method": "POST",
           "url": "http://localhost:5000/api/evento",
          "data": {"nomEvento": "Assessor",
                  }
    }
]

rotasEventoGetPutGet = [
    {
        "method": "GET",
        "url": "http://127.0.0.1:5000/api/evento"
    },
    {
        "method": "PUT",
           "url": "http://localhost:5000/api/evento",
          "data": {"codEvento": 3, "nomEvento": "Assessor Legislativo",
                  }
    },
    {
        "method": "GET",
           "url": "http://127.0.0.1:5000/api/evento"
    },
]

rotasEventoDelete = [
    {"method": "DELETE",
        "url": "http://localhost:5000/api/evento/3"
    },
]
