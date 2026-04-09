function runSystem(){

    let road = document.getElementById("road").value;
    let density = document.getElementById("density").value;
    let waiting = document.getElementById("waiting").value;
    let emergency = document.getElementById("emergency").value;

    let data = {
        A:{density:10,waiting:10},
        B:{density:10,waiting:10},
        C:{density:10,waiting:10},
        D:{density:10,waiting:10}
    };

    data[road] = {density,waiting};

    fetch('/predict',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify(data)
    })
    .then(res=>res.json())
    .then(res=>{

        let priority = res.priority;
        let time = res.roads[priority].signal;

        if(emergency != 0){
            priority = road;
            time *= 1.5;
            spawnEmergency(priority, emergency);
            playSound();
        }

        startSignal(priority, time);
    });
}


// 🚦 SIGNAL CONTROL + TIMER
function startSignal(priority, time){

    resetLights();

    if(priority==="A") northLight.innerText="🟢";
    if(priority==="B") southLight.innerText="🟢";
    if(priority==="C") eastLight.innerText="🟢";
    if(priority==="D") westLight.innerText="🟢";

    moveCars(priority);

    countdown(time);
}


// 🔴 RESET
function resetLights(){
    northLight.innerText="🔴";
    southLight.innerText="🔴";
    eastLight.innerText="🔴";
    westLight.innerText="🔴";
}


// 🚗 CAR MOVEMENT
function moveCars(priority){

    if(priority==="A") carN.style.top="200px";
    if(priority==="B") carS.style.bottom="200px";
    if(priority==="C") carE.style.right="200px";
    if(priority==="D") carW.style.left="200px";
}


// ⏱ TIMER
function countdown(time){
    let t = Math.floor(time);
    let interval = setInterval(()=>{
        document.getElementById("timer").innerText = "⏱ "+t+" sec";
        t--;
        if(t<0) clearInterval(interval);
    },1000);
}


// 🚑 EMERGENCY VEHICLE
function spawnEmergency(road, type){

    let vehicle = document.createElement("div");

    if(type==1) vehicle.innerText="🚑";
    if(type==2) vehicle.innerText="🚒";
    if(type==3) vehicle.innerText="🚓";

    vehicle.style.position="absolute";
    vehicle.style.top="250px";
    vehicle.style.left="250px";

    document.getElementById("roadBox").appendChild(vehicle);

    setTimeout(()=>vehicle.remove(),3000);
}


// 🔊 SOUND
function playSound(){
    let audio = new Audio("https://www.soundjay.com/buttons/beep-07.wav");
    audio.play();
}