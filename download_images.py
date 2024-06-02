import requests,sys,json,os,csv
from PIL import Image

categorize = sys.argv[1]
save_folder = './images/'+categorize+'/'

# Json 和 CSV 文件和.github\workflows\douban.yml保持一致
# 只能二选一，不用的那个留空，否则会报错

# 如果是 Json 文件使用下面这一行
json_file_path = './data/'+categorize+'/movie.json'
json_book_path = './data/'+categorize+'/book.json'
# json_file_path = ''

# 如果是 CSV 文件使用下面这一行
# csv_movie_path = './data/douban/movie.csv'
csv_movie_path= ''
# 这里是book的csv路径
# csv_book_path = './douban/book.csv'
csv_book_path= ''

def exists(path):
  if path == '': return False
  return os.path.exists(path)
  
def download_image_by_json(json_item):
  for i in json_item: 
    image_url = i['subject']['cover_url']
    #image_url = i['subject']['pic']['large']
    # id.jpg
    #file_name = i['subject']['id']+'.'+image_url.split('.')[-1] 
    file_name = i['subject']['id']+'.jpg'
    dowoload_file(image_url, file_name) 

def download_image_by_csv(data_csv):
  for row in data_csv:
    image_url = row[3]
    #file_name = row[0]+'.'+image_url.split(".")[-1]
    file_name = row[0]+'.jpg'
    dowoload_file(image_url, file_name) 
  
def dowoload_file(image_url, file_name):
  # 确保文件夹路径存在
  os.makedirs(save_folder, exist_ok=True)
  if image_url.startswith("https://") and "koobai.com" in image_url:
    # 请求头
    headers = {
    'Referer': 'https://koobai.com'
    } 
  else:
    headers = {
    'Referer': 'https://doubanio.com'
    }
  response = requests.get(image_url, headers=headers, timeout=30)
  #file_name = image_url.split('/')[-1]
  save_path = os.path.join(save_folder, file_name)
  if check_image(save_path):
    print(f'文件已存在 {file_name}')
  else:
    print('文件不存在')
    with open(save_path, 'wb') as file:
      file.write(response.content)
    print(f'图片已保存为 {file_name}')

def check_image(image_path):
  if os.path.exists(image_path):
    try:
        Image.open(image_path).verify()
        print(f"{image_path} is a valid image")
        return True
    except:
        print(f"{image_path} is not a valid image")
        os.remove(image_path)
        return False
  else:
    return False

if(exists(json_file_path)):
  print('我是Movies Json文件，开始执行。。。。。')
  with open(json_file_path, 'r', encoding='utf-8') as file:
    data_json = json.load(file)
  # 提取URL字段的值
    download_image_by_json(data_json)
elif(exists(csv_movie_path)):
  print('我是Movies CSV文件，开始执行。。。。。')
  data_csv = []  # 存储数据的列表
  with open(csv_movie_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)  # 创建 CSV 读取器对象
        next(csv_reader)  # 跳过标题行
        for row in csv_reader:  # 逐行读取数据
            data_csv.append(row)  # 将每行数据添加到列表中
    # 打印数据
  download_image_by_csv(data_csv)
else:
  print('。。。。。。。跳过电影图片下载')

data_book = []
if(exists(json_book_path)):
  print('我是Book Json文件，开始执行。。。。。')
  with open(json_book_path, 'r', encoding='utf-8') as file:
    data_json = json.load(file)
  # 提取URL字段的值
    download_image_by_json(data_json)
elif(exists(csv_book_path)):
  print('我是Book CSV文件，开始执行。。。。。')
  with open(csv_book_path, 'r', encoding='utf-8') as books:
    csv_books = csv.reader(books)
    next(csv_books)
    for book in csv_books:  # 逐行读取数据
      data_book.append(book)
    # 打印数据
    download_image_by_csv(data_book)
else:
  print('。。。。。。。跳过书籍图片下载')
    
