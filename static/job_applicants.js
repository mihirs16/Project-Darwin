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
    
    fetch("http://localhost:5000/data/admin/getCandidates/" + jobId.toString(), { method: 'GET' })
    .then(response => response.json())
    .then(result => displayCandidateList(result))
    .catch(error => console.log('error', error));
}

function getResume (id) {
    jobId = parseInt(document.getElementById("meta").innerText);
    key = jobId.toString() + "_" + id.toString();
    window.open("http://localhost:5000/data/getResume/" + key.toString())
}

function drawPercentile (obj) {
    // const percentile = (arr, val) => (100 * arr.reduce((acc, v) => acc + (v < val ? 1 : 0) + (v === val ? 0.5 : 0), 0)) / arr.length;
    // per = []
    // for (i=0;i<ovr.length;i++) {
    //     per.push(percentile (ovr, ovr[i]));
    // }
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
    jobId = parseInt(document.getElementById("meta").innerText);

    var requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };
      
    fetch("http://localhost:5000/data/admin/getJobStats/" + jobId.toString(), requestOptions)
    .then(response => response.json())
    .then((result) => drawPlots(result))
    .catch(error => console.log('error', error));
}