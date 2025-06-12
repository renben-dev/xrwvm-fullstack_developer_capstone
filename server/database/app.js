const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const  cors = require('cors');
const app = express();
const port = 3030;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));

const reviews_data = JSON.parse(fs.readFileSync("reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("dealerships.json", 'utf8'));

mongoose.connect("mongodb://mongo_db:27017/",{'dbName':'dealershipsDB'});

const Reviews = require('./review');
const Dealerships = require('./dealership');

// try {
//   Reviews.deleteMany({}).then(()=>{
//     Reviews.insertMany(reviews_data['reviews']);
//   });
//   Dealerships.deleteMany({}).then(()=>{
//     Dealerships.insertMany(dealerships_data['dealerships']);
//   });

// } catch (error) {
//   res.status(500).json({ error: 'Error fetching documents' });
// }
//renzo: I refactored the above block so 1.the original blok does not use await inside
//so error may not be catch-ed properly
//2.made the two data operations in paraller
(async () => {
    try {
      const reviewsOps = (async () => {
        await Reviews.deleteMany({});
        await Reviews.insertMany(reviews_data.reviews);
      })();

      const dealersOps = (async () => {
        await Dealerships.deleteMany({});
        await Dealerships.insertMany(dealerships_data.dealerships);
      })();

      await Promise.all([reviewsOps, dealersOps]);

      console.log('Database reset successfully');
    } catch (error) {
      console.error('Error resetting database:', error);
    }
  })();


// Express route to home
app.get('/', async (req, res) => {
    res.send("Welcome to the Mongoose API");
});


// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});


// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({dealership: req.params.id});
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});


// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
//Write your code here
    try {
        const dealerships_objs = await Dealerships.find();
        res.json(dealerships_objs);
    } catch (error) {
        res.status(500).json({error: 'Error fetching dealerships data'});
    }
});


// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
//Write your code here
    try {
        const documents = await Dealerships.find({state: req.params.state});
        res.json(documents);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching dealership' });
    }
});


// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
//Write your code here
try {
    const documents = await Dealerships.find({id: req.params.id});
    res.json(documents);
} catch (error) {
    res.status(500).json({ error: 'Error fetching dealership' });
}
});


//Express route to insert review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  data = JSON.parse(req.body);

  //renzo: below 2 lines are refactored below
  //const documents = await Reviews.find().sort( { id: -1 } )
  //let new_id = documents[0]['id']+1

  //renzo: refactoring to avoid sorting ALL the documents in js
  //not that mongodb applies any filtering/sorting first, before findOne is applied
  const document = await Reviews.findOne().sort({ id: -1 });
  let new_id = 1;
  if(document){
    new_id = document.id + 1;
  }

  const review = new Reviews({
        "id": new_id,
        "name": data.name,
        "dealership": data.dealership,
        "review": data.review,
        "purchase": data.purchase,
        "purchase_date": data.purchase_date,
        "car_make": data.car_make,
        "car_model": data.car_model,
        "car_year": data.car_year,
	});

  try {
    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
        console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});


// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
