from flask import Flask,request,jsonify,render_template
from captionbot import CaptionBot
import os
import json
import urllib2
from BeautifulSoup import BeautifulSoup
import requests
from werkzeug.utils import secure_filename
##UPLOAD_FOLDER = 'F:\\major related\\flaskapp\\uploads'
UPLOAD_FOLDER=''
app = Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

url='http://vqa.daylen.com/'
header = {"Cookie": "__cfduid=dea235a1d1a47fd34e362c90c4edc22a21495359987; __utma=130288904.146958539.1495359990.1495406506.1495443228.4; __utmb=130288904.3.10.1495443228; __utmc=130288904; __utmz=130288904.1495359990.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)","User-Agent":"Chrome/58.0.3029.110"}

@app.route('/gettype',methods=['GET'])
def gettype():
	msgtype=request.args.get('type')
	return jsonify({'message':'your type was '+msgtype})
@app.route('/')
def hello():
    #return app.send_static_file('webspeech.html')
    #return app.send_static_file('anyangspeech.html')
	return "hello , welcome"
@app.route('/describe',methods=['POST'])
def describe():
	msgtype=request.form['type']
	##question=request.form['question']
	print(str(msgtype) + "is message ")
	imagefile=request.files['imagefile']
	filename=secure_filename(imagefile.filename)
	imagefile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	print(filename)
	filepath=os.path.join(app.config['UPLOAD_FOLDER'], filename)
	print(filepath)
	if(msgtype=='1'):
		c=CaptionBot()
		print("caption bot running")
		result=c.file_caption(filepath)
		print(result)
		return jsonify({'message':result,'type':msgtype,'filename':filename,'filepath':filepath})
	elif(msgtype=='2'):
		question=request.form['question']
		##establish connection
		##if (question is None) return jsonify({'message':'error , didnt include question','type':'2'})
		response = requests.get(url, headers=header)
		
		##upload image
		url1 = 'http://vqa.daylen.com/api/upload_image'
		files={'file': open(filepath,'rb')}
		response = requests.post(url1, files=files,headers=header)
		data = json.loads(response.text)
		im_id=data['img_id']
		print im_id
		## upload question
		url2 = 'http://vqa.daylen.com/api/upload_question'
		#'fa10956c0743670ec5c924ce1523ab16'
		datas={'img_id':im_id, 'question':question}
		response = requests.post(url2,data=datas ,headers=header)
		##get response
		print(response.text)
		data = json.loads(response.text)
		return jsonify({'message':data[u'answer'],'type':'2'})
	else:
		return jsonify({'message': 'error in type ','type':'1'})
if __name__ == '__main__':
   app.run()
