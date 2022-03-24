let port = "5699";
let data = [];



function sendChangeServerResponse(response) {
  console.log("sendChangeServerResponse", response);
  if(response == "False" || typeof response == "undefined" || response == null) {
    ;
  }
  else{
    let port = "5699";
    chrome.storage.sync.get(['port'], function(result) {
      if(result.data == undefined || result.data == null) {
        port = "5699";
      }
      else{
          port = result.data;
      }

      let url = "http://localhost:" + port + "/";
      console.log("url", url);
      console.log("inside", response);

      let sendAlert = {
        "message": "CHANGE_SERVER"
      };

      
      // alert("SafeSearch is on");


      // (async () => {
      //   const rawResponse = await fetch(url, {
      //     method: 'POST',
      //     headers: {
      //       'Accept': '*/*',
      //       // 'Content-Type': 'application/json'
      //     },
      //     // body: JSON.stringify({a: 1, b: 'Textual content'})
      //     body: JSON.stringify({message: response})
      //   });
      //   const content = await rawResponse;
      
      //   // console.log(content);
      // })();
    

      function f() {
        console.log("Trying...")
        fetch(url, {
          method: 'POST',
          headers: {
            'Accept': '*/*',
            // 'Content-Type': 'application/json'
          },
          // body: JSON.stringify({a: 1, b: 'Textual content'})
          body: JSON.stringify({message: response})
        })
        .then(function(data) {
            console.log('succeeded', data)
        }).catch(function(error) {
            console.log('request failed', error)
            setTimeout(f, 3000);
        });
      }

      f();

    });
  }
}


chrome.tabs.onUpdated.addListener( function (tabId, changeInfo, tab) {
  if (changeInfo.status == 'complete') {
    chrome.scripting.executeScript({
      target: {tabId: tabId},
      files: ["scraper.js"]
    });
    // console.log(data[i].textToSearch);

    setTimeout(function() {
      chrome.tabs.sendMessage(tab.id, {text: ""}, function(response) {
        console.log("outside", response);
        sendChangeServerResponse(response);
      });
    }, 1000);
  }
});


