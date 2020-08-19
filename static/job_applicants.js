function loadView (id) {
    if (!id) {
        document.getElementById("appl").style = "color: white; background-color: #1971c2;";
        document.getElementById("all-applicants").style.display = 'block';

        document.getElementById("dash").style = "color: #1971c2; background: none;"
        document.getElementById("dashboard").style.display = 'none';
    } else {
        document.getElementById("dash").style = "color: white; background-color: #1971c2;";
        document.getElementById("dashboard").style.display = 'block';

        document.getElementById("appl").style = "color: #1971c2; background: none;"
        document.getElementById("all-applicants").style.display = 'none';
    }
}

function displayCandidateList (result) {
    console.log (result.length);
    allCandy = document.getElementById("all-applicants"); 
    candyTemplate = document.getElementById("this-applicant");
    
    for (i = 0; i < result.length; i++) {
        newCandy = candyTemplate.cloneNode(true);
        newCandy.getElementsByClassName("resumebtn")[0].setAttribute("onclick", "getResume(" + result[i]['id'].toString() + ");");
        // newCandy.getElementById("emailbtn").appendChild()
        newCandy.getElementsByClassName("candy-name")[0].innerText = result[i]['name'];
        newCandy.getElementsByClassName("candy-mail")[0].innerText = result[i]['email'];
        newCandy.getElementsByClassName("candy-score")[0].innerText = (result[i]['score'].toFixed(2)*100).toString() + "%";
        allCandy.appendChild(newCandy);
    }
}

function loadCandidateList () {
    jobId = parseInt(document.getElementById("meta").innerText);
    
    fetch("https://project-darwin.azurewebsites.net/data/admin/getCandidates/" + jobId.toString(), { method: 'GET' })
    .then(response => response.json())
    .then((result) => {
        displayCandidateList(result);
        console.log("Here");
        getJobStats();
        document.getElementById("selecttop").setAttribute("onclick", "selectCandy();");
    })
    .catch(error => console.log('error', error));
}

function getResume (id) {
    jobId = parseInt(document.getElementById("meta").innerText);
    key = jobId.toString() + "_" + id.toString();
    window.open("https://project-darwin.azurewebsites.net/data/getResume/" + key.toString())
}

function drawPercentile (obj) {
    var trace1 = {
        x: obj['x'],
        y: obj['y'],
        type: 'bar'
    };
    var data = [trace1];
    Plotly.newPlot('percentile', data, { plot_bgcolor: "#e7f5ff" });
}

function drawSkills (obj) {
    var trace1 = {
        x: obj['x'],
        y: obj['y'],
        type: 'bar',
        orientation: 'h'
    };
    var data = [trace1];
    Plotly.newPlot('skill', data, { plot_bgcolor: "#e7f5ff" });
}

function drawDOJ (obj) {
    var trace1 = {
        x: obj['x'],
        y: obj['y'],
        type: 'bar'
    };
    var data = [trace1];
    Plotly.newPlot('doj', data, { plot_bgcolor: "#e7f5ff" });
}

function drawYOE (obj) {
    var trace1 = {
        x: obj['x'],
        y: obj['y'],
        type: 'line'
    };
    var data = [trace1];
    Plotly.newPlot('yoe', data, { plot_bgcolor: "#e7f5ff" });
}

function drawPlots (result) {
    drawPercentile (result['perc']);
    drawSkills (result['ski']);
    drawDOJ (result['doj']);
    drawYOE (result['yoe']);
}

function getJobStats () {
    console.log("Here Again");
    jobId = parseInt(document.getElementById("meta").innerText);

    var requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };
      
    fetch("https://project-darwin.azurewebsites.net/data/admin/getJobStats/" + jobId.toString(), requestOptions)
    .then(response => response.json())
    .then((result) => drawPlots(result))
    .catch(error => console.log('error', error));
}

function selectCandy () {
    document.getElementById("overlay").style.display = "flex";
    document.getElementById("emailqt").setAttribute("max", (document.getElementsByClassName("candy-mail").length-1).toString())
}

function sendMails () {
    var allEmailElems = document.getElementsByClassName("candy-mail");
    var allEmails = [];
    for (i=0; i<allEmailElems.length; i++) {
        allEmails.push(allEmailElems[i].innerText.toString());
    }
    valEma = parseInt(document.getElementById("emailqt").value) + 1
    // console.log(valEma)
    allEmails = allEmails.slice(1, valEma);
    console.log(allEmails);

    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    fetch("https://project-darwin.azurewebsites.net/sendEmails", {
            method: 'POST',
            headers: myHeaders,
            body: JSON.stringify({"emails":allEmails})
    })
    .then(response => response.text())
    .then((result) => {
        document.getElementById("overlay").style.display = "none";
        alert('Mails Sent!');
    })
    .catch(error => console.log('error', error));
}