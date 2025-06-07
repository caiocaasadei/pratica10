
rotasCargoPost = [
    {
        "method": "POST",
           "url": "http://localhost:5000/api/cargo",
          "data": {"nomCargo": "Assessor",
                  }
    }
]

rotasCargoGetPutGet = [
    {
        "method": "GET",
        "url": "http://127.0.0.1:5000/api/cargo"
    },
    {
        "method": "PUT",
           "url": "http://localhost:5000/api/cargo",
          "data": {"codCargo": 3, "nomCargo": "Assessor Legislativo",
                  }
    },
    {
        "method": "GET",
           "url": "http://127.0.0.1:5000/api/cargo"
    },
]

rotasCargoDelete = [
    {"method": "DELETE",
        "url": "http://localhost:5000/api/cargo/3"
    },
]
