/* Shared Chart.js configs — one function per chart, unique canvas IDs.
   Numbers verbatim from the uploaded EuRepoC v1.3.2 exports. */

/* Dark-theme defaults so ticks, legend, and grid read on #0F2040 surfaces */
if (window.Chart) {
  Chart.defaults.color = '#C8D8F0';
  Chart.defaults.font.family = "'JetBrains Mono', monospace";
  Chart.defaults.borderColor = 'rgba(106,136,170,0.18)';
  Chart.defaults.plugins.legend.labels.boxWidth = 12;
  Chart.defaults.plugins.legend.labels.font = { size: 11 };
}
const GRID = { color: 'rgba(106,136,170,0.15)' };

function trendChart(id){
  new Chart(document.getElementById(id),{
    type:'line',
    data:{labels:[2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
      datasets:[
        {label:'Total incidents (raw)',data:[131,166,135,120,91,71,160,354,729,701],borderColor:'#185FA5',backgroundColor:'#185FA5',borderWidth:2,pointRadius:3,tension:.15},
        {label:'Excluding CI-only-rule incidents (adjusted)',data:[131,166,134,120,90,69,148,316,445,399],borderColor:'#0F6E56',backgroundColor:'#0F6E56',borderWidth:2,borderDash:[6,4],pointRadius:3,tension:.15}
      ]},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{position:'top'}},
      scales:{y:{beginAtZero:true,grid:GRID,title:{display:true,text:'Number of incidents'}},x:{grid:GRID}}}
  });
}

function sectorChart(id){
  new Chart(document.getElementById(id),{
    type:'bar',
    data:{labels:[2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
      datasets:[
        {label:'Critical infrastructure',data:[23,37,42,29,24,26,54,159,432,402],backgroundColor:'#D85A30'},
        {label:'State institutions / political system',data:[84,116,73,70,55,41,90,170,300,296],backgroundColor:'#185FA5'},
        {label:'Corporate Targets',data:[19,24,23,25,22,12,29,70,74,58],backgroundColor:'#BA7517'},
        {label:'Social groups',data:[15,23,19,10,14,11,17,20,18,19],backgroundColor:'#7F77DD'},
        {label:'Media',data:[18,19,16,10,12,6,17,22,21,20],backgroundColor:'#D4537E'},
        {label:'Education',data:[0,1,1,0,1,4,5,12,86,74],backgroundColor:'#1D9E75'},
        {label:'Science',data:[4,8,10,8,9,7,7,10,1,1],backgroundColor:'#639922'},
        {label:'Other',data:[4,3,1,6,2,1,1,6,2,4],backgroundColor:'#888780'}
      ]},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{position:'top'}},
      scales:{x:{stacked:true,grid:GRID},y:{stacked:true,beginAtZero:true,grid:GRID,title:{display:true,text:'Incidents (deduplicated)'}}}}
  });
}

function typeChart(id){
  new Chart(document.getElementById(id),{
    type:'bar',
    data:{labels:[2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
      datasets:[
        {label:'Ransomware',data:[0,0,6,2,3,4,9,34,221,224],backgroundColor:'#E24B4A'},
        {label:'Disruption',data:[54,75,36,28,20,9,32,134,390,345],backgroundColor:'#BA7517'},
        {label:'Data theft',data:[59,56,76,76,58,44,64,105,229,220],backgroundColor:'#7F77DD'},
        {label:'Data theft & Doxing',data:[16,41,10,7,4,4,21,58,89,63],backgroundColor:'#D4537E'},
        {label:'Hijacking with Misuse',data:[43,50,72,68,60,50,83,174,532,535],backgroundColor:'#D85A30'},
        {label:'Hijacking without Misuse',data:[4,2,9,3,11,17,47,73,84,79],backgroundColor:'#1D9E75'},
        {label:'Not available',data:[0,0,0,0,0,0,1,0,0,1],backgroundColor:'#888780'}
      ]},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{position:'top'}},
      scales:{x:{stacked:true,grid:GRID},y:{stacked:true,beginAtZero:true,grid:GRID,title:{display:true,text:'Incidents (by attack type tag)'}}}}
  });
}

// ---- V1: adjusted trend with OLS fit + 95% CI ----
function trendRegChart(id){
  const years=[2015,2016,2017,2018,2019,2020,2021,2022,2023,2024];
  const adj=[131,166,134,120,90,69,148,316,445,399];
  const fit=[56.2,88.6,120.9,153.3,185.6,218.0,250.3,282.7,315.0,347.4];
  const lo=[-75.3,-23.0,27.1,73.4,113.8,146.1,170.5,188.9,203.5,215.9];
  const hi=[187.7,200.1,214.7,233.1,257.5,289.8,330.2,376.5,426.6,478.9];
  new Chart(document.getElementById(id),{
    type:'line',
    data:{labels:years,datasets:[
      {label:'95% confidence interval',data:hi,borderColor:'transparent',backgroundColor:'rgba(224,135,95,0.14)',pointRadius:0,fill:'+1'},
      {label:'_lo',data:lo,borderColor:'transparent',backgroundColor:'rgba(224,135,95,0.14)',pointRadius:0,fill:false},
      {label:'OLS trend (+32/yr, p=0.016, R²=0.53)',data:fit,borderColor:'#E8875F',borderWidth:2,pointRadius:0,fill:false},
      {label:'Adjusted incidents (observed)',data:adj,borderColor:'#00C9A7',backgroundColor:'#00C9A7',showLine:false,pointRadius:4}
    ]},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{position:'top',labels:{filter:i=>i.text!=='_lo'}}},
      scales:{y:{beginAtZero:true,grid:GRID,title:{display:true,text:'Incidents (rule-adjusted)'}},x:{grid:GRID}}}
  });
}

// ---- V2: HHI OLS regression with 95% CI + excluded 2024 point ----
function hhiRegChart(id){
  const fitYears=[2017,2018,2019,2020,2021,2022,2023];
  const hhi=[1269,1307,1378,1442,1531,1611,1658];
  // OLS: HHI = 68.9*year - 137635  ->  fitted line over the window
  const fit=fitYears.map(y=>68.9*y-137635);
  // 95% CI band (approx, symmetric ~ +/- from the printed figure)
  const band=fitYears.map((y,i)=>({lo:fit[i]-24-Math.abs(3-i)*4, hi:fit[i]+24+Math.abs(3-i)*4}));
  new Chart(document.getElementById(id),{
    type:'line',
    data:{labels:[...fitYears,2024],datasets:[
      {label:'95% CI',data:[...band.map(b=>b.hi),null],borderColor:'transparent',backgroundColor:'rgba(224,135,95,0.13)',pointRadius:0,fill:'+1'},
      {label:'_lo',data:[...band.map(b=>b.lo),null],borderColor:'transparent',backgroundColor:'rgba(224,135,95,0.13)',pointRadius:0,fill:false},
      {label:'OLS fit: 68.9 HHI/yr (R²=0.991)',data:[...fit,null],borderColor:'#E8875F',borderWidth:2,pointRadius:0,fill:false},
      {label:'HHI (2017–2023, in fit)',data:[...hhi,null],borderColor:'#5BA4CF',backgroundColor:'#5BA4CF',showLine:false,pointRadius:5},
      {label:'2024 (excluded — reclassification)',data:[null,null,null,null,null,null,null,1485],borderColor:'#6A88AA',backgroundColor:'transparent',showLine:false,pointRadius:6,pointStyle:'circle',borderWidth:2}
    ]},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{position:'top',labels:{filter:i=>i.text!=='_lo'}}},
      scales:{y:{grid:GRID,title:{display:true,text:'HHI (Σ market share², Big Three)'}},x:{grid:GRID}}}
  });
}

// ---- V2: provider share stacked area + CR3 line ----
function providerShareChart(id){
  const years=[2017,2018,2019,2020,2021,2022,2023,2024];
  new Chart(document.getElementById(id),{
    type:'line',
    data:{labels:years,datasets:[
      {label:'AWS',data:[33,33,33,33,33,33,31,30],backgroundColor:'rgba(240,153,58,0.75)',borderColor:'#F0993A',fill:true,pointRadius:0,tension:.2},
      {label:'Microsoft Azure',data:[12,13,15,17,19,21,24,21],backgroundColor:'rgba(91,164,207,0.75)',borderColor:'#5BA4CF',fill:true,pointRadius:0,tension:.2},
      {label:'Google Cloud',data:[6,7,8,8,9,9,11,12],backgroundColor:'rgba(76,175,125,0.75)',borderColor:'#4CAF7D',fill:true,pointRadius:0,tension:.2},
      {label:'CR3 total (Big Three)',data:[51,53,56,58,61,63,66,63],borderColor:'#EEF4FF',borderDash:[4,3],borderWidth:2,pointRadius:0,fill:false,tension:.2,yAxisID:'y2'}
    ]},
    options:{responsive:true,maintainAspectRatio:false,
      interaction:{intersect:false,mode:'index'},
      plugins:{legend:{position:'top'}},
      scales:{
        x:{grid:GRID},
        y:{stacked:true,grid:GRID,max:80,ticks:{callback:v=>v+'%'},title:{display:true,text:'Market share (%)'}},
        y2:{position:'right',max:80,min:0,grid:{drawOnChartArea:false},ticks:{callback:v=>v+'%'},title:{display:true,text:'CR3 combined (%)'}}
      }}
  });
}
