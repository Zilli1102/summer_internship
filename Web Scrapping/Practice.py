from bs4 import BeautifulSoup

def load_html(file_path):
    with open(file_path,"r",encoding="utf-8") as f:
        content=f.read()
        #print(content)
        return content

def extract_posts(soup):
    post_elements=soup.find_all(name="div",class_="person")
    posts=[]
    #print(post_elements)
    for post in post_elements:
        name=post.find(name="h1",class_="name").text
        city= post.find(name="h2", class_="city").text
        company = post.find(name="h3", class_="company").text
        designation = post.find(name="p", class_="designation").text

        posts.append({'name':name,'city':city,'company':company,'designation':designation})
    return posts

html_content=load_html("Gunj.html")
#print(html_content)

soup=BeautifulSoup(html_content,features="html.parser")
posts=extract_posts(soup)
#print(posts)

for post in posts:
    print(f"name: {post['name']}, city: {post['city']}, company: {post['company']}")

    print("----------------------------------------")