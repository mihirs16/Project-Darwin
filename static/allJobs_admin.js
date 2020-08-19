getAllJobs();

function spawnJobs (results) {
    console.log(results.length)
    console.log("spawning")
    carSec = document.getElementById("career-section");
    for (i = 0; i < results.length; i++) {
        if (i % 3) {
            console.log(i.toString() + " card")
            jobCardTemplate = document.getElementsByClassName('col m-3 p-3 jobcard')[0];
            newJobCard = jobCardTemplate.cloneNode(true);
            href = "https://project-darwin.azurewebsites.net/applicants/" + results[i]['id'].toString();
            newJobCard.setAttribute("onclick", "location.href='"+href+"'");            
            newJobCard.getElementsByClassName("jobtitle")[0].innerText = results[i]['role'];
            newJobCard.getElementsByClassName("joblocation")[0].innerText = results[i]['loc'].split(", ").join(" | ");
            newJobCard.getElementsByClassName("altdet")[0].children[0].innerText = results[i]['des'];
            newJobCard.getElementsByClassName("altdet")[0].children[1].innerText = results[i]['skill'].split(", ").join(" | ");
            newJobCard.getElementsByClassName("altdet")[0].children[2].innerText = "Experience: " + results[i]['yoe'].toString() + " Years";
            
            thisInnerRow.appendChild(newJobCard);
        } else {            
            console.log(i.toString() + " row")
            thisRow = document.createElement('div');
            thisRow.style = "display: flex; justify-content: center;";
            thisInnerRow = document.createElement('div');
            thisInnerRow.className = "row";
            thisRow.appendChild(thisInnerRow);
            carSec.appendChild(thisRow);

            console.log(i.toString() + " card")
            jobCardTemplate = document.getElementsByClassName('col m-3 p-3 jobcard')[0];
            newJobCard = jobCardTemplate.cloneNode(true);
            href = "https://project-darwin.azurewebsites.net/applicants/" + results[i]['id'].toString();
            newJobCard.setAttribute("onclick", "location.href='"+href+"'");           
            newJobCard.getElementsByClassName("jobtitle")[0].innerText = results[i]['role'];
            newJobCard.getElementsByClassName("joblocation")[0].innerText = results[i]['loc'].split(", ").join(" | ");
            newJobCard.getElementsByClassName("altdet")[0].children[0].innerText = results[i]['des'];
            newJobCard.getElementsByClassName("altdet")[0].children[1].innerText = results[i]['skill'].split(", ").join(" | ");
            newJobCard.getElementsByClassName("altdet")[0].children[2].innerText = "Experience: " + results[i]['yoe'].toString() + " Years";
            
            thisInnerRow.appendChild(newJobCard);
        }
    }
}

function getAllJobs () {
    console.log("Fetching");
    fetch ("https://project-darwin.azurewebsites.net/data/getAllJobs", {method: 'GET'})
    .then (response => response.json ())
    .then (result => spawnJobs (result))
    .catch (error => console.log ('error', error));
}