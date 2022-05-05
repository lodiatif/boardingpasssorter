
# Boarding Pass Sorter  
  
A library and a wrapper RESTful API that accepts boarding passes in random order and   
sorts them in correct itinerary order.  
  
### Code Organisation  
  
The project is built in Django framework using [Django REST framework](https://www.django-rest-framework.org) for the   
RESTful API.  
  
One of the packages in root folder is `core` which is an independent library that models the entities in the problem domain  
and contains the business logic.  
  
#### Core library  
The `core` consists of 2 modules: a `lib` module and a `tests` module.  
  
Lib module is essentially the entire library that contains models and business logic.  
  
Tests module consists of test cases.  
  
### Setup dev environment (Unix based - Linux or Mac)  
To setup development environment follow the instructions below  
1. Clone the repository  
Open terminal and change directory to where you wish to clone the repository  
```shell  
git clone https://github.com/lodiatif/boardingpasssorter.git
```  
  
Once cloned, change to the root directory of the project and create Python3 virtual-environment and install required packages.  
  
```shell  
cd boardingpasssorterpython3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```  
  
Once the virtual environment is set, run the following command to run `core` library tests  
```shell  
export PYTHONPATH=$PYTHONPATH:.
python -m unittest core/tests.py
```  
  
### RESTful API usage  
There is only 1 API hosted: `/apis/sort_trips/`  
It supports GET and POST methods. GET simply returns sample request structure for different travel modes.  
  
 #### Input explained
POST request takes a JSON array where each node represents a boarding pass (or a trip).  
Here is an example of a JSON node that represents boarding pass of a train trip:  
  
```json  
{
    "transport": {
        "platform_number": "7",
        "vehicle_id": "T-12",
        "seat_number": "B65",
        "mode": "Train"
    },
    "destination": {
        "location": {
            "name": "Buffalo",
            "station": "BUF",
            "city": "New York"
        }
    },
    "source": {
        "location": {
            "name": "Syracuse",
            "station": "SYR",
            "city": "New York"
        }
    }
}
```  
  
Each boarding pass node has 3 elements:   
  
**transport**  
Holds input specific to the mode of transport.
  
  | Property | Is Mandatory | Description | Possible Values |
|---|---|---|---|
| mode | Yes | Indicates mode of transportation | Bus, Train, Airplane  | 
| vehicle_id | Yes | Vehicle identifier |  |
| seat_number | No | Seat number in the vehicle |  |
| platform_number | No | Can optionally provide for Train |  |
| gate_number | Yes (only for Airplane) | Indicates gate number for departure | |
| baggage_counter | No | Can optionally provide for Airplane |  |


**source**
Holds inputs specific to source location of the trip

**destination**
Holds inputs specific to destination location of the trip

Both source and destination have one property called `location` with the following properties:

  | Property | Is Mandatory | Description |
|---|---|---|
| name | Yes | Name of the location |
| city | Yes | City of the location |
| station | Yes | Code identifying the airport, bus stop or train station |

Here's a sample `POST` request input containing 2 boarding passes in incorrect order:

```json
[
    {
        "transport": {
            "baggage_counter": "344",
            "vehicle_id": "ABC",
            "gate_number": "3A",
            "seat_number": "B65",
            "mode": "Airplane"
        },
        "destination": {
            "location": {
                "name": "Albany",
                "station": "ALB",
                "city": "New York"
            }
        },
        "source": {
            "location": {
                "name": "Buffalo",
                "station": "BUF",
                "city": "New York"
            }
        }
    },
    {
        "transport": {
            "platform_number": "7",
            "vehicle_id": "T-12",
            "seat_number": "B65",
            "mode": "Train"
        },
        "destination": {
            "location": {
                "name": "Buffalo",
                "station": "BUF",
                "city": "New York"
            }
        },
        "source": {
            "location": {
                "name": "Syracuse",
                "station": "SYR",
                "city": "New York"
            }
        }
    }
]
```

 #### Output explained
Output is the sorted list of trips to complete the journey. Note: It has N+1th element that narrates end of journey.

Output sample for the above input:
```json
[
    "1. Take train T-12 from Syracuse (SYR) railway station in New York to Buffalo (BUF) railway station in New York. Seat # B65 Platform # 7",
    "2. Take flight ABC from Buffalo (BUF) airport in New York to Albany (ALB) airport in New York. Seat # B65, gate 3A. Baggage drop at counter 344",
    "3. You have arrived at your final destination."
]
```


#### Using RESTful API (in browser)

Run the Django development server.

While in the root directory of the project, run the following command

```shell
python manage.py runserver
```

if you see the following line at the end, it is an indicator that server is running:
```shell
Quit the server with CONTROL-C.
```
In your browser, go to  [http://127.0.0.1:8000/apis/sort_trips/](http://127.0.0.1:8000/apis/sort_trips/)
You should see the browsable API page generated by Django REST framework.
Scroll down to see a form that accepts POST request. Simply copy-paste the sample and click on `POST`, the form will submit a POST request to the same API which returns the desired output.


## Adding a new transportation mode
A new transportation mode can be added by extending 2 areas in the core library.
1. TransportMode
This class acts as an enum of transportation modes supported by the library. Any new transportation mode should be added to this enum, along with changes to its support functions for the new transportation.
2. Extend a new class from `TravelPass` abstract class.
The new class should simply call super.init in its init method, and optionally set indigenous properties for narration purposes. Can refer to `TrainTravelPass.platform_number` to see how to add an indigenous property.

Once these 2 changes are made, new tests may be added in the tests module to make sure the changes haven't introduced regression and are functionally working as expected.