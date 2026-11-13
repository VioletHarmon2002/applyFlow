const companyInput = document.getElementById("company");
const positionInput = document.getElementById("position");
const statusInput = document.getElementById("status");

const form = document.getElementById("job-form");

const list = document.getElementById("job-list"); // creating job list
const filter = document.getElementById("status-filter");

let applications = [];

const editModal = document.getElementById("edit-modal");


// Initialization
//loadApplications();
//updateApplications();

//submitting the form
form.addEventListener("submit", (event) =>{
    event.preventDefault();
    const formData = new FormData(form);
    const job = Object.fromEntries(formData); // convert to one object

    if(!job.company.trim() || !job.position.trim()) {
        alert("All fields are required")
        return;
    } 
    job.company = job.company.trim(); // removes spaces
    job.position = job.position.trim();

    createApplication(job);
});

// filtering 
filter.addEventListener("change", (e) => {
    
    updateApplications();
})


function displayApplications(jobs) {
    list.textContent="";
    jobs.forEach((job) => {
        

        const li = document.createElement("li");
        li.textContent = (`${job.company}, ${job.position}, ${job.status}`);

        list.appendChild(li);
        console.log(list);

        const dltbtn = document.createElement("button");
        Object.assign(dltbtn, {textContent: "Delete", className: "delete-button", name: "delete"});

        const editbtn = document.createElement("button");
        Object.assign(editbtn, {textContent: "Edit", className: "edit-btn", name: "edit"});

        li.appendChild(dltbtn);
        li.appendChild(editbtn);
        dltbtn.addEventListener("click" , (e)=> {
            deleteApplication(job.id);
        })
        // edit event listener
        editbtn.addEventListener("click", (e)=>{
            editApplication(job.id);
        })

    })
    
    

}

function editApplication(id) {
    let index = applications.findIndex(job => job.id == id)
    if (index !== -1) {
        editModal.showModal();

    }
}
function deleteApplication(id) {
  let index = applications.findIndex(job => job.id === id );
  if (index !== -1 ) {
    applications.splice(index, 1 )
  }
  saveApplications();
  updateApplications();
  
}    

//update of applications
function updateApplications() {
    const selectedresult = filter.value;
    let filterresult;
    if(selectedresult === "All") {
        filterresult = applications;
    } else {
        filterresult = applications.filter(appl => appl.status === selectedresult);

    }
    displayApplications(filterresult);
    
}

//local storage saving
function saveApplications() {
    localStorage.setItem("applications", JSON.stringify(applications)); //saves array of applications like JSON json.stringify() to save the structure of objects
    //JSON.stringify() does not modify the original array, but creates a new string. applications is still an array
}
//loading from local strorage
function loadApplications() {
    const saved = localStorage.getItem("applications"); // gets string applications. gets string or null
    if (saved !== null) {
        try {
           const savedjs = JSON.parse(saved) //Restores the JavaScript value back, localStorage keeps only Strings
           console.log(savedjs);
           if (Array.isArray(savedjs)) {

            applications.push(... savedjs )
           }
        } catch (error) {
            console.log("Invalid saved JSON");
        } 
    } else {
        console.log("No saved job");
    }
}

async function getApplications() {
    const request = new Request("http://localhost:8000/applications", {
        method: "GET",
    });
    try {
        const response = await fetch(request); //fetch - функция JavaScript, которая отправляет HTTP-запрос на сервер(backend). response	Хранит HTTP-ответ

    
    if (!response.ok) {
        throw new Error("Error")
    } 
    const data = await response.json()//Читает и преобразует JSON в JavaScript-значение
    applications = data;
    displayApplications(data); 
    console.log(data)

    } catch (error) {
        console.error(error);
    }
}
getApplications() 

async function createApplication(job) {
    const request = new Request("http://localhost:8000/applications", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(job) //convert a JavaScript object into a JSON string before sending it to FastAPI.
    });
    try {
        const response = await fetch(request);

    if (!response.ok) {
        throw new Error("Error")
    }
    const data = await response.json()   //JSON из HTTP-ответа → JavaScript value
    getApplications();
    console.log(data)

    } catch (error) {
        console.log(error)
    }

}

async function deleteApplication(id) {
    const request = new Request(
        `http://localhost:8000/applications/${id}`,
        {
            method: "DELETE"
        }
    );

    try {
        const response = await fetch(request);

        if (!response.ok) {
            throw new Error("Failed to delete application");
        }

        await getApplications();

    } catch (error) {
        console.error(error);
    }
}


