"""Shopping tools for finding products and deals."""

from langchain.tools import tool
from typing import Optional


@tool
def get_store_products(store: Optional[str] = None, category: Optional[str] = None):
    """Get popular products from stores.
    
    Args:
        store: Store name (amazon, walmart, target, etc.)
        category: Product category (electronics, clothing, books, etc.)
    
    Returns:
        Array of product objects
    """
    try:
        if category == "electronics" or not category:
            return [
                {
                    "title": "Wireless Earbuds Pro",
                    "store": store or "Amazon",
                    "original_price": "$99.99",
                    "price": "$79.99",
                    "discount": "20%",
                    "rating": "4.8/5",
                    "link": "https://amazon.com/s?k=wireless+earbuds+pro"
                },
                {
                    "title": "Smart Watch Series 8",
                    "store": store or "Best Buy",
                    "original_price": "$349.99",
                    "price": "$299.99",
                    "discount": "14%",
                    "rating": "4.7/5",
                    "link": "https://www.bestbuy.com/site/searchpage.jsp?st=smart+watch+series+8"
                },
                {
                    "title": "Portable SSD 1TB",
                    "store": store or "Walmart",
                    "original_price": "$129.99",
                    "price": "$89.99",
                    "discount": "31%",
                    "rating": "4.6/5",
                    "link": "https://www.walmart.com/search?q=portable+ssd+1tb"
                },
                {
                    "title": "USB-C Hub 7-in-1",
                    "store": store or "Amazon",
                    "original_price": "$49.99",
                    "price": "$34.99",
                    "discount": "30%",
                    "rating": "4.5/5",
                    "link": "https://amazon.com/s?k=usb+c+hub+7+in+1"
                },
                {
                    "title": "4K Webcam Ultra HD",
                    "store": store or "Best Buy",
                    "original_price": "$169.99",
                    "price": "$129.99",
                    "discount": "24%",
                    "rating": "4.7/5",
                    "link": "https://www.bestbuy.com/site/searchpage.jsp?st=4k+webcam"
                },
                {
                    "title": "Mechanical Keyboard RGB",
                    "store": store or "Amazon",
                    "original_price": "$199.99",
                    "price": "$149.99",
                    "discount": "25%",
                    "rating": "4.8/5",
                    "link": "https://amazon.com/s?k=mechanical+keyboard+rgb"
                },
                {
                    "title": "Wireless Mouse Compact",
                    "store": store or "Walmart",
                    "original_price": "$39.99",
                    "price": "$24.99",
                    "discount": "38%",
                    "rating": "4.6/5",
                    "link": "https://www.walmart.com/search?q=wireless+mouse"
                },
                {
                    "title": "Monitor 27-inch 144Hz",
                    "store": store or "Best Buy",
                    "original_price": "$399.99",
                    "price": "$299.99",
                    "discount": "25%",
                    "rating": "4.9/5",
                    "link": "https://www.bestbuy.com/site/searchpage.jsp?st=27+inch+144hz+monitor"
                },
                {
                    "title": "Phone Stand Adjustable",
                    "store": store or "Amazon",
                    "original_price": "$24.99",
                    "price": "$14.99",
                    "discount": "40%",
                    "rating": "4.5/5",
                    "link": "https://amazon.com/s?k=phone+stand+adjustable"
                },
                {
                    "title": "Power Bank 25000mAh",
                    "store": store or "Target",
                    "original_price": "$59.99",
                    "price": "$39.99",
                    "discount": "33%",
                    "rating": "4.7/5",
                    "link": "https://www.target.com/s?searchTerm=power+bank+25000"
                }
            ]
        elif category == "books":
            return [
                {
                    "title": "Atomic Habits",
                    "author": "James Clear",
                    "store": store or "Amazon",
                    "original_price": "$27.99",
                    "price": "$15.99",
                    "discount": "43%",
                    "rating": "4.9/5",
                    "link": "https://amazon.com/s?k=atomic+habits+james+clear"
                },
                {
                    "title": "The Midnight Library",
                    "author": "Matt Haig",
                    "store": store or "Barnes & Noble",
                    "original_price": "$28.99",
                    "price": "$17.99",
                    "discount": "38%",
                    "rating": "4.7/5",
                    "link": "https://www.barnesandnoble.com/s/midnight+library"
                },
                {
                    "title": "Project Hail Mary",
                    "author": "Andy Weir",
                    "store": store or "Amazon",
                    "original_price": "$28.99",
                    "price": "$18.99",
                    "discount": "34%",
                    "rating": "4.8/5",
                    "link": "https://amazon.com/s?k=project+hail+mary+andy+weir"
                },
                {
                    "title": "The Lean Startup",
                    "author": "Eric Ries",
                    "store": store or "Amazon",
                    "original_price": "$30.99",
                    "price": "$16.99",
                    "discount": "45%",
                    "rating": "4.6/5",
                    "link": "https://amazon.com/s?k=lean+startup+eric+ries"
                },
                {
                    "title": "Thinking Fast and Slow",
                    "author": "Daniel Kahneman",
                    "store": store or "Barnes & Noble",
                    "original_price": "$30.00",
                    "price": "$19.99",
                    "discount": "33%",
                    "rating": "4.7/5",
                    "link": "https://www.barnesandnoble.com/s/thinking+fast+and+slow"
                },
                {
                    "title": "The Power of Now",
                    "author": "Eckhart Tolle",
                    "store": store or "Amazon",
                    "original_price": "$25.99",
                    "price": "$14.99",
                    "discount": "42%",
                    "rating": "4.8/5",
                    "link": "https://amazon.com/s?k=power+of+now+eckhart+tolle"
                },
                {
                    "title": "Educated",
                    "author": "Tara Westover",
                    "store": store or "Target",
                    "original_price": "$29.99",
                    "price": "$17.99",
                    "discount": "40%",
                    "rating": "4.9/5",
                    "link": "https://www.target.com/s?searchTerm=educated+tara+westover"
                },
                {
                    "title": "The 7 Habits of Highly Effective People",
                    "author": "Stephen Covey",
                    "store": store or "Amazon",
                    "original_price": "$28.99",
                    "price": "$16.99",
                    "discount": "41%",
                    "rating": "4.7/5",
                    "link": "https://amazon.com/s?k=7+habits+stephen+covey"
                },
                {
                    "title": "Sapiens",
                    "author": "Yuval Noah Harari",
                    "store": store or "Barnes & Noble",
                    "original_price": "$35.00",
                    "price": "$18.99",
                    "discount": "46%",
                    "rating": "4.8/5",
                    "link": "https://www.barnesandnoble.com/s/sapiens"
                },
                {
                    "title": "The Innovators",
                    "author": "Walter Isaacson",
                    "store": store or "Amazon",
                    "original_price": "$30.00",
                    "price": "$19.99",
                    "discount": "33%",
                    "rating": "4.6/5",
                    "link": "https://amazon.com/s?k=innovators+walter+isaacson"
                }
            ]
        elif category == "clothing":
            return [
                {
                    "title": "Cotton T-Shirt Bundle",
                    "store": store or "Target",
                    "original_price": "$44.99",
                    "price": "$24.99",
                    "discount": "44%",
                    "rating": "4.6/5",
                    "link": "https://www.target.com/s?searchTerm=cotton+t-shirt"
                },
                {
                    "title": "Denim Jeans Classic Fit",
                    "store": store or "Gap",
                    "original_price": "$89.99",
                    "price": "$59.99",
                    "discount": "33%",
                    "rating": "4.5/5",
                    "link": "https://www.gap.com/browse/category.do?cid=1011"
                },
                {
                    "title": "Running Shoes Pro",
                    "store": store or "Nike",
                    "original_price": "$179.99",
                    "price": "$129.99",
                    "discount": "28%",
                    "rating": "4.7/5",
                    "link": "https://www.nike.com/w?q=running+shoes"
                },
                {
                    "title": "Casual Hoodie Comfort",
                    "store": store or "Target",
                    "original_price": "$54.99",
                    "price": "$34.99",
                    "discount": "36%",
                    "rating": "4.7/5",
                    "link": "https://www.target.com/s?searchTerm=hoodie"
                },
                {
                    "title": "Yoga Pants Premium",
                    "store": store or "Lululemon",
                    "original_price": "$128.00",
                    "price": "$98.99",
                    "discount": "23%",
                    "rating": "4.8/5",
                    "link": "https://shop.lululemon.com/c/womens-leggings"
                },
                {
                    "title": "Leather Jacket Black",
                    "store": store or "Nordstrom",
                    "original_price": "$299.99",
                    "price": "$199.99",
                    "discount": "33%",
                    "rating": "4.7/5",
                    "link": "https://www.nordstrom.com/s/leather+jacket"
                },
                {
                    "title": "Summer Dress Floral",
                    "store": store or "H&M",
                    "original_price": "$69.99",
                    "price": "$39.99",
                    "discount": "43%",
                    "rating": "4.6/5",
                    "link": "https://www2.hm.com/en_us/women/products/dresses.html"
                },
                {
                    "title": "Wool Sweater Cozy",
                    "store": store or "Target",
                    "original_price": "$74.99",
                    "price": "$44.99",
                    "discount": "40%",
                    "rating": "4.7/5",
                    "link": "https://www.target.com/s?searchTerm=wool+sweater"
                },
                {
                    "title": "Sports Shorts Quick Dry",
                    "store": store or "Adidas",
                    "original_price": "$79.99",
                    "price": "$54.99",
                    "discount": "31%",
                    "rating": "4.8/5",
                    "link": "https://www.adidas.com/us/search?q=sports+shorts"
                },
                {
                    "title": "Winter Boots Waterproof",
                    "store": store or "REI",
                    "original_price": "$199.99",
                    "price": "$139.99",
                    "discount": "30%",
                    "rating": "4.8/5",
                    "link": "https://www.rei.com/s?query=winter+boots"
                }
            ]
        else:
            return [
                {
                    "title": "Popular Item 1",
                    "store": store or "Amazon",
                    "price": "$29.99",
                    "rating": "4.5/5",
                    "link": "https://amazon.com"
                },
                {
                    "title": "Trending Item 2",
                    "store": store or "Walmart",
                    "price": "$39.99",
                    "rating": "4.6/5",
                    "link": "https://walmart.com"
                },
                {
                    "title": "Best Seller 3",
                    "store": store or "Target",
                    "price": "$49.99",
                    "rating": "4.7/5",
                    "link": "https://target.com"
                },
                {
                    "title": "Top Rated 4",
                    "store": store or "Amazon",
                    "price": "$59.99",
                    "rating": "4.8/5",
                    "link": "https://amazon.com"
                },
                {
                    "title": "Customer Favorite 5",
                    "store": store or "Best Buy",
                    "price": "$69.99",
                    "rating": "4.7/5",
                    "link": "https://bestbuy.com"
                },
                {
                    "title": "New Release 6",
                    "store": store or "Target",
                    "price": "$44.99",
                    "rating": "4.6/5",
                    "link": "https://target.com"
                },
                {
                    "title": "Budget Friendly 7",
                    "store": store or "Walmart",
                    "price": "$19.99",
                    "rating": "4.5/5",
                    "link": "https://walmart.com"
                },
                {
                    "title": "Premium Choice 8",
                    "store": store or "Amazon",
                    "price": "$89.99",
                    "rating": "4.9/5",
                    "link": "https://amazon.com"
                },
                {
                    "title": "Limited Edition 9",
                    "store": store or "Best Buy",
                    "price": "$79.99",
                    "rating": "4.8/5",
                    "link": "https://bestbuy.com"
                },
                {
                    "title": "Best Value 10",
                    "store": store or "Target",
                    "price": "$34.99",
                    "rating": "4.7/5",
                    "link": "https://target.com"
                }
            ]
    except Exception as e:
        return []
