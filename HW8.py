# Your name: 
# Your student id:
# Your email:
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute("SELECT r.name, c.category, b.building, r.rating FROM restaurants r "
                   "JOIN categories c ON r.category_id = c.id "
                   "JOIN buildings b ON r.building_id = b.id")
    rows = cursor.fetchall()

    restaurants = {}
    for row in rows:
        name, category, building, rating = row
        if name not in restaurants:
            restaurants[name] = {"category": category, "building": building, "rating": rating}

    cursor.close()
    conn.close()

    return restaurants


def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute("SELECT categories.category, COUNT(*) FROM restaurants INNER JOIN categories ON restaurants.category_id = categories.id GROUP BY categories.category")
    rows = cursor.fetchall()

    categories = {}
    for row in rows:
        category, count = row
        categories[category] = count

    cursor.close()
    conn.close()

    # create a bar chart
    plt.bar(categories.keys(), categories.values())
    plt.title("Number of restaurants by category")
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.show()
    return categories

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Join restaurants and building_restaurant tables and filter by building number
    cursor.execute("SELECT r.name FROM restaurants r INNER JOIN buildings br ON r.building_id = br.id WHERE br.building = ? ORDER BY r.rating DESC", (building_num,))

    rows = cursor.fetchall()

    # Convert rows to a list of restaurant names
    restaurant_list = [row[0] for row in rows]

    cursor.close()
    conn.close()
    return restaurant_list


#EXTRA CREDIT
def get_highest_rating(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Query to get the highest-rated restaurant category and its average rating
    cursor.execute("SELECT c.category, AVG(r.rating) FROM restaurants r JOIN categories c ON r.category_id = c.id GROUP BY c.id ORDER BY AVG(r.rating) DESC LIMIT 1")
    category_data = cursor.fetchone()

    # Query to get the building with the highest-rated restaurants and its average rating
    cursor.execute("SELECT b.building, AVG(r.rating) FROM restaurants r JOIN buildings b ON r.building_id = b.id GROUP BY b.id ORDER BY AVG(r.rating) DESC LIMIT 1")
    building_data = cursor.fetchone()

    # Query to get the data for the category bar chart
    cursor.execute("SELECT c.category, AVG(r.rating) FROM restaurants r JOIN categories c ON r.category_id = c.id GROUP BY c.id ORDER BY AVG(r.rating) DESC")
    category_rows = cursor.fetchall()

    # Query to get the data for the building bar chart
    cursor.execute("SELECT b.id, AVG(r.rating) FROM restaurants r JOIN buildings b ON r.building_id = b.id GROUP BY b.id ORDER BY AVG(r.rating) DESC")
    building_rows = cursor.fetchall()

    cursor.close()
    conn.close()

    # Create the data for the category bar chart
    category_labels = [row[0] for row in category_rows]
    category_ratings = [row[1] for row in category_rows]

    # Create the data for the building bar chart
    building_labels = [row[0] for row in building_rows]
    building_ratings = [row[1] for row in building_rows]

    # Create and show the category bar chart
    plt.figure(figsize=(8,6))
    plt.barh(category_labels, category_ratings)
    plt.xlabel("Average rating")
    plt.ylabel("Category")
    plt.title("Average ratings by restaurant category")
    plt.show()

    # Create and show the building bar chart
    plt.figure(figsize=(8,6))
    plt.barh(building_labels, building_ratings)
    plt.xlabel("Average rating")
    plt.ylabel("Building")
    plt.title("Average ratings by building")
    plt.show()

    return [(category_data[0], category_data[1]), (building_data[0], building_data[1])]

#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
