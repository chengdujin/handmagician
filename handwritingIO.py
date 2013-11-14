# -*- coding: utf-8 -*-
import urllib,urllib2
import json
import sys


def getHWResult(bData):
	"""
	bData: string or list
		eg: "102a186a103a186a105a186a107a185"
		or: [
				[(102,186),(103,186),(105,186),(107,185)],
				[...]
			]
	result: {'s':'candicate words','t':1 or 3 or -1}
		t=1: ok
		t=3: api error, input cannot be recognised
		t=-1: network error

	example: firstWord = list(handwritingIO.getHWResult('11a12a11a13a11a14a11a15a11a16')['s'])[0]

	"""
	data = {'wd':'','type':1}
	if(isinstance(bData,list)):
		newBData = []
		for x in bData:
			for i in x:
				newBData.extend(list(i))
		bData = 'a'.join(map(lambda x:str(x),newBData))
		print bData
	if(isinstance(bData,basestring)):
		bData = bData.strip('a')
		data['wd'] = bData
	try:
		f=urllib2.urlopen(
			url="http://hw.baidu.com",
			data=urllib.urlencode(data)
		)
		r=json.loads(f.read())
	except Exception, e:
		r={'s':'Network Error.','t':-1}
	return r

if __name__ == "__main__":
	if(len(sys.argv)<2):
		print 'usage: python '+sys.argv[0]+' 102a186a103a186a105a186a107a185'
	else:
		r = list(getHWResult(sys.argv[1])['s'])
		print '\t'.join(r)
