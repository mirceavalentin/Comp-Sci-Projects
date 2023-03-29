var authorlist= []

const form = document.getElementById('tableform');
const submitButton = document.getElementById('submitbutton');

/* Sumbit data in JSON with an AJAX POST fetch request dynamically 
   added to the HTML gallery */

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const author = document.getElementById('author').value;   
    const image = document.getElementById('image').value;
    const alt = document.getElementById('alt').value;
    const tags = document.getElementById('tags').value;
    const description = document.getElementById('description').value;

    const formData = new FormData(event.target);
    formData.append('author', author); 
    formData.append('image', image);
    formData.append('alt', alt);
    formData.append('tags', tags);
    formData.append('description', description);  

    const imageGallery = document.getElementById('imageGallery');
    const newDiv= document.createElement('div')
    const newAuthor = document.createElement('p');
    newAuthor.innerHTML = author;
    const newImage = document.createElement('img');
    newImage.src = image;
    const newImageBox = document.createElement('p')
    const newAlt = document.createElement('p');
    newAlt.innerHTML = alt;
    const newTags = document.createElement('p');
    newTags.innerHTML = tags;
    const newDescription = document.createElement('p');
    newDescription.innerHTML = description;
    
    newDiv.appendChild(newAuthor);
    newDiv.appendChild(newImage);
    newImageBox.appendChild(newImage);
    newDiv.append(newImageBox);
    newDiv.appendChild(newAlt);
    newDiv.appendChild(newTags);
    newDiv.appendChild(newDescription);
    imageGallery.appendChild(newDiv);

    const div = document.getElementsByTagName('div')[0];
    div.appendChild(newDiv);


    try {
        const response = await fetch("http://localhost:4000/authors", {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(Object.fromEntries(formData))
        });
        if(!response.ok){
            throw new Error(response.statusText);
        }
        form.reset();
    }
    catch(error){
        alert(`error occured: ${error}`);
    }
    location.reload()
    });
    
    // AJAX GET request to insert JSON data into the gallery 

    fetch("http://localhost:4000/authors", {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(Object.fromEntries)
})
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        addData(data); 

    })
    .catch(error => {
        console.error(`Error: ${error.message}`);
    });

    //new buttons for authors and filter function

    addedauthors= new Set();
    function addData(data) {
        authorlist=data;
       
        var mainBox = document.getElementById("imageGallery");
        for (var i = 0; i < data.length; i++) {
            if (!addedauthors.has(data[i].author.toUpperCase())) {
                var div = document.createElement("div");
                div.innerHTML = `<p class= author> ${data[i].author}</p>` + `<img src=${data[i].image} alt=${data[i].alt}>` + `<p class= alt> ${data[i].alt}</p>` + `<p class= tags> ${data[i].tags}</p>` + `<p class= description> ${data[i].description}</p>`;
                div.className="imageBox";
                mainBox.appendChild(div);
                button = document.createElement("button")
                button.innerHTML=data[i].author;
                button.className="filterButton"
                button.value=data[i].author;
                document.getElementById("authorButtons").appendChild(button)
                addedauthors.add(data[i].author.toUpperCase())
            }
        } 
        clickFilter()
    }
    
function clickFilter(){
    buttons1 = document.querySelectorAll(".filterButton")
    var mainBox = document.getElementById("imageGallery");

    for(let i=0; i<buttons1.length;i++){
        buttons1[i].addEventListener("click", function(){
            mainBox.innerHTML="";
            for(let j=0; j<authorlist.length;j++){
                if(authorlist[j].author==buttons1[i].innerHTML){
                    var div = document.createElement("div");
                    div.innerHTML = `<p class= author> ${authorlist[j].author}</p>` + `<img src=${authorlist[j].image} alt=${authorlist[j].alt}>` + `<p class= alt> ${authorlist[j].alt}</p>` + `<p class= tags> ${authorlist[j].tags}</p>` + `<p class= description> ${authorlist[j].description}</p>`;
                    div.className="imageBox";
                    mainBox.appendChild(div)
                }};
        });
    }};

//reset button 
const resetbutton = document.getElementById("resetbutton");
resetbutton.addEventListener("click", function(){
    fetch("http://localhost:4000/authors", {
        method: "GET"
    })
    .then(data => {
        form.reset()
        console.log("Successful reset");
    })
    .catch(error => {
        console.log("Error: ", error);
    });
    location.reload()
});



const updatebutton = document.getElementById("updatebutton");
updatebutton.addEventListener("click", function(){
    const id = 7; // replace with the ID of the image you want to update
    const author = document.getElementById('author').value;
    const image = document.getElementById('image').value;
    const alt = document.getElementById('alt').value;
    const tags = document.getElementById('tags').value;
    const description = document.getElementById('description').value;

    const updateData = { author, image, alt, tags, description };

    fetch(`https://wt.ops.labs.vu.nl/api23/ddc9d54c/item/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(updateData)
    })
    .then(response => {
        if(!response.ok){
            throw new Error(response.statusText);
        }
        console.log("Successfully updated image with ID: ", id);
    })
    .catch(error => {
        console.log("Error: ", error);
    });
});
