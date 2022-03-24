function save(){
  let entriesDiv = document.getElementById("entries");
  let entries = entriesDiv.getElementsByClassName("entry");
  let data = [];

  for(let i = 0; i < entries.length; i++){
    let entry = entries[i];
    let entryData = {
      "hostname": entry.getElementsByClassName("hostname")[0].value,
      "textToSearch": entry.getElementsByClassName("textToSearch")[0].value
    }
    data.push(entryData);
  }

  //console.log(data);

  chrome.storage.sync.set({"data": data}, function() {
    console.log('Value is set to ', data);

    chrome.storage.sync.get(['data'], function(result) {
      console.log('Value currently is : ' + result.data.length, result.data);
    });
  });


  document.getElementById("settings_saved_text").style.display = "inline-block";
  setTimeout(function(){
    document.getElementById("settings_saved_text").style.display = "none";
    chrome.storage.sync.get(['data'], function(result) {
      console.log('Value currently is : ' + result.data.length, result.data);
    });
  }, 2000);

}


function entryDeleteListenerSetter(){
  //console.log("entryDeleteListenerSetter");

  let deleteBtns = document.getElementsByClassName("deleteBtn");

  
  deleteBtns[deleteBtns.length - 1].addEventListener("click", function(event){
    //console.log(event);
    let entry = event.target.parentElement;;
    entry.remove();
  });
}


function createInputFields(){
  let entriesDiv = document.getElementById("entries");

  let entryDiv = document.createElement('div');
  entryDiv.classList.add('entry');
  
  let entriesLength = 0;

  // chrome.storage.sync.get(['data'], function(result) {
  //   if(result.data != undefined){
  //     console.log('Value currently is : ' + result.data.length, result.data);
  //     entries = result.data;
  //     entriesLength = result.data.length;

      entryDiv.innerHTML = `
      <p class="id">#.</p>
      <label for="hostname">Website Hostname:</label>
      <input type="text" class="hostname" name="hostname" placeholder="i.e. google.com"><br><br>
      <label for="lname">Text to search:</label>
      <input type="text" class="textToSearch" name="textToSearch" placeholder="i.e. cats"><br><br>
      <button class="deleteBtn">Delete</button>
      <hr/>
      `;

      entriesDiv.appendChild(entryDiv);
      entryDeleteListenerSetter();
    // }
  // });
}

function displayEntries(){
  //console.log("displayEntries");
  chrome.storage.sync.get(['data'], function(result) {
    if(result.data != undefined){
      console.log('Value currently is : ' + result.data.length, result.data);
      entries = result.data;
      entriesDiv = document.getElementById("entries");
      entriesDiv.innerHTML = "";
      for(let i = 0; i < entries.length; i++){
        let entry = entries[i];
        let entryDiv = document.createElement('div');
        entryDiv.classList.add('entry');
        entryDiv.innerHTML = `
          <p class="id">#${i+1}</p>
          <label for="hostname">Website Hostname:</label>
          <input type="text" class="hostname" name="hostname" value="${entry.hostname}"><br><br>
          <label for="lname">Text to search:</label>
          <input type="text" class="textToSearch" name="textToSearch" value="${entry.textToSearch}"><br><br>
          <button class="deleteBtn">Delete</button>
          <hr/>
        `;

        entriesDiv.appendChild(entryDiv);
        
        entryDeleteListenerSetter();
      }
    }
  });
}

document.getElementById("addBtn").addEventListener("click", createInputFields);
document.getElementById("saveBtn").addEventListener("click", save);

displayEntries();