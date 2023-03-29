
const sqlite = require('sqlite3').verbose();
let db = my_database('./gallery.db');
const joi = require(`joi`);

// ###############################################################################
// The database should be OK by now. Let's setup the Web server so we can start
// defining routes.
//
// First, create an express application `app`:

var express = require("express");
var app = express();

// We need some middleware to parse JSON data in the body of our HTTP requests:
app.use(express.json());



app.get('/authors', (req, res) => {   //See all authors
	db.all("SELECT author, alt, tags, image, description FROM gallery", (err, row) => {
    	if (err || (row.lenght == 0)) {
            return console.error(err);
        }

        return res.status(200).header('Acces-Control-Allow-Origin', '*').send(JSON.stringify(row));
    });
});

app.get('/authors/:id', (req, res) => {     //See an author by id
    db.all("SELECT * FROM gallery WHERE id=?", [req.params.id], (err, row) => {
        if (err || (row.length === 0)){
            console.error(err.message);
            return res.status(404).json({"error":"ID not found"});
        }
        return res.status(200).header('Content-Type', 'application/json').send(JSON.stringify(row));
    });
});

app.delete('/authors/:id', (req, res) => {    //Delete function
    db.run("DELETE FROM gallery WHERE id=" + [req.params.id], (err, row) => {
        
		if(err || (row.length === 0)){
            console.log(req.body);
            return res.status(404).json({"error":"ID not found"});
        };
        console.log(req.body);
        return res.status(204).header('Access-Control-Allow-Origin', "*");
    });
});

app.post('/authors', (req, res) => {	    //Posting a new row in the database
    const {error} = validator(req.body);
    if(error){
        return res.status(400).json({"error":"Missing field"});
    }
    db.run(`INSERT INTO gallery (author, alt, tags, image, description) VALUES (?, ?, ?, ?, ?)`, [`${req.body.author}`, `${req.body.alt}`, `${req.body.tags}`, `${req.body.image}`, `${req.body.description}`], (err, row) => {
        
		if(err){
            return console.error(err);
        }

        console.log(req.body);
	    return res.status(201).header('Access-Control-Allow-Origin', '*');

    });
});

app.put('/authors/:id', (req, res) => {
    var id = req.params.id;
    db.run(`update gallery author=${JSON.stringify(req.body.author)}, alt=${JSON.stringify(req.body.alt)},tags=${JSON.stringify(req.body.tags)}, image=${JSON.stringify(req.body.image)}, description=${JSON.stringify(req.body.description)} where id = ${id}`, (err) => {
        if (err) {
            throw err.message;
        }
    });
});

function validator(p) {
    const schema = joi.object({
        id: joi.number(),
        author: joi.string().min(1).max(40).required(),
        alt: joi.string().min(5).max(100).required(),
        tags: joi.string().min(1).max(60).required(),
        image: joi.string().min(1).max(500).required(),
        description: joi.string().min(1).max(500).required(),
    })

    console.log(schema.validate(p));
    return schema.validate(p);
};


// ###############################################################################

app.listen(3000);
console.log("Your Web server should be up and running, waiting for requests to come in........");

function my_database(filename) {
	var db = new sqlite.Database(filename, (err) => {
  		if (err) {
			console.error(err.message);
  		}
  		console.log('Connected to the database.');
	});
	db.serialize(() => {
		db.run(`
        	CREATE TABLE IF NOT EXISTS gallery
        	 (
                    id INTEGER PRIMARY KEY,
                    author CHAR(100) NOT NULL,
                    alt CHAR(100) NOT NULL,
                    tags CHAR(256) NOT NULL,
                    image char(2048) NOT NULL,
                    description CHAR(1024) NOT NULL
		 )
		`);
		db.all(`select count(*) as count from gallery`, function(err, result) {
			if (result[0].count == 0) {
				db.run(`INSERT INTO gallery (author, alt, tags, image, description) VALUES (?, ?, ?, ?, ?)`, [
        			"Tim Berners-Lee",
        			"Image of Berners-Lee",
        			"html,http,url,cern,mit",
        			"https://upload.wikimedia.org/wikipedia/commons/9/9d/Sir_Tim_Berners-Lee.jpg",
        			"The internet and the Web aren't the same thing."
    				]);
				db.run(`INSERT INTO gallery (author, alt, tags, image, description) VALUES (?, ?, ?, ?, ?)`, [
        			"Grace Hopper",
        			"Image of Grace Hopper at the UNIVAC I console",
        			"programming,linking,navy",
        			"https://upload.wikimedia.org/wikipedia/commons/3/37/Grace_Hopper_and_UNIVAC.jpg",
				"Grace was very curious as a child; this was a lifelong trait. At the age of seven, she decided to determine how an alarm clock worked and dismantled seven alarm clocks before her mother realized what she was doing (she was then limited to one clock)."
    				]);
				console.log('Inserted dummy photo entry into empty database');
			} else {
				console.log("Database already contains", result[0].count, " item(s) at startup.");
			}
		});
	});
	return db;
}
