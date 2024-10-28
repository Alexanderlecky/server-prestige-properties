from app import app
from models import db, House

with app.app_context():
    db.create_all()
houses = [
    {
        "id": 1,
        "name": "Luxury Villa in Kilimani",
        "location": "Kilimani, Nairobi",
        "price": 500000,
        "image": "https://cdn.pixabay.com/photo/2019/11/12/17/48/villa-4621636_640.jpg",
        "description": "A luxurious villa located in the heart of Kilimani, Nairobi. This villa offers modern amenities and ample space for comfortable living."
    },
    {
        "id": 2,
        "name": "Beachfront Apartment in Mombasa",
        "location": "Mombasa, Kenya",
        "price": 300000,
        "image": "https://cdn.pixabay.com/photo/2020/03/21/20/03/real-estate-4955087_640.jpg",
        "description": "This beachfront apartment in Mombasa provides stunning views of the ocean and access to white sandy beaches. Ideal for vacation living."
    },
    {
        "id": 3,
        "name": "Mountain Retreat in Naivasha",
        "location": "Naivasha, Kenya",
        "price": 400000,
        "image": "https://cdn.pixabay.com/photo/2019/11/26/19/41/villa-4655352_640.jpg",
        "description": "Nestled in the mountains of Naivasha, this retreat offers breathtaking scenery and a peaceful atmosphere perfect for nature lovers."
    },
    {
        "id": 4,
        "name": "Penthouse in Westlands",
        "location": "Westlands, Nairobi",
        "price": 750000,
        "image": "https://cdn.pixabay.com/photo/2020/03/21/20/03/real-estate-4955086_640.jpg",
        "description": "A modern penthouse in the bustling neighborhood of Westlands, Nairobi. This property boasts panoramic city views and luxurious amenities."
    },
    {
        "id": 5,
        "name": "Farmhouse in Nanyuki",
        "location": "Nanyuki, Kenya",
        "price": 600000,
        "image": "https://cdn.pixabay.com/photo/2024/04/16/06/28/ai-generated-8699185_640.jpg",
        "description": "A spacious farmhouse located in Nanyuki, Kenya. Surrounded by scenic landscapes, it's ideal for a rural lifestyle or a retreat."
    },
    {
        "id": 6,
        "name": "Contemporary Loft in Karen",
        "location": "Karen, Nairobi",
        "price": 450000,
        "image": "https://cdn.pixabay.com/photo/2022/07/09/05/23/house-7310177_640.jpg",
        "description": "This stylish contemporary loft in Karen offers a unique blend of comfort and modern design, perfect for urban living."
    },
    {
        "id": 7,
        "name": "Lakefront Villa in Kisumu",
        "location": "Kisumu, Kenya",
        "price": 550000,
        "image": "https://cdn.pixabay.com/photo/2017/04/10/22/28/residence-2219972_640.jpg",
        "description": "A lakefront villa with beautiful views of Lake Victoria in Kisumu. This property is ideal for relaxation and waterside living."
    },
    {
        "id": 8,
        "name": "Modern Apartment in Thika",
        "location": "Thika, Kenya",
        "price": 250000,
        "image": "https://cdn.pixabay.com/photo/2017/03/30/00/24/villa-2186906_640.jpg",
        "description": "A modern apartment in Thika that offers convenience and comfort, located near shopping centers and amenities."
    },
    {
        "id": 9,
        "name": "Beach House in Diani",
        "location": "Diani, Kenya",
        "price": 550000,
        "image": "https://cdn.pixabay.com/photo/2020/04/28/04/03/villa-5102547_640.jpg",
        "description": "This beach house in Diani provides direct access to the ocean and a serene environment. Perfect for a coastal lifestyle."
    },
    {
        "id": 10,
        "name": "Country Cottage in Limuru",
        "location": "Limuru, Kenya",
        "price": 350000,
        "image": "https://cdn.pixabay.com/photo/2018/02/13/11/09/home-3150500_640.jpg",
        "description": "A charming country cottage in Limuru, surrounded by lush greenery and perfect for a peaceful retreat."
    }
]

# Use the app context to access the database
with app.app_context():
    # Clear existing houses in the database before adding new ones
    db.session.query(House).delete()

    for house in houses:
        new_house = House(
            name=house["name"],
            location=house["location"],
            price=house["price"],
            image=house["image"],
            description=house["description"]
        )
        db.session.add(new_house)

    db.session.commit()
    print("Seed data added successfully!")