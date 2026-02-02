const { MongoClient } = require('mongodb');
const fs = require('fs');

const uri = "mongodb://localhost:27017";
const client = new MongoClient(uri);

async function load_Data() {
    try {
        await client.connect();
        const db = client.db('fleximart');
        const collection = db.collection('products');

        // Read and parse JSON file
        const data = JSON.parse(fs.readFileSync('./products_catalog.json', 'utf-8'));

        // Insert data
        const result = await collection.insertMany(data);
        console.log(`${result.insertedCount} documents were inserted`);
    } catch (err) {
        console.error(err);
    } finally {
        await client.close();
    }
}
// load_Data();

async function find(){
    try {
        await client.connect();
        const db = client.db('fleximart');
        const collection = db.collection('products');
        
        const my_fields = {
            name: 1,
            price: 1,
            _id: 0 // Exclude the _id field, which is included by default
        };

        const result = await collection.find()

}