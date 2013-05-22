import urllib2
import json
import sys


opener = urllib2.build_opener()

def loadPage(url):
    req = urllib2.Request(url)
    f = opener.open(req)
    return json.load(f)


def getFileData(file):
    data = loadPage(file['resource'])

    return {
        'name'    : data.get('name', None),
        'language': data.get('language', None),
        'geshi'   : data.get('geshi', None),
        'content' : data.get('content', None)
    }

def extractFilesFromFolder(folder, language= None):
    files = []

    data = loadPage(folder['resource'])
    for f in data.get('files', []):
        fileData = getFileData(f)
        if fileData['language'] == language:
            files.append({
                'uri' : f['resource'],
                'data': fileData
            })

    for d in data.get('folders', []):
        files += extractFilesFromFolder(d)

    return files

def extractFilesFromContribution(member, language=None):
    files = []
    try:
        data = loadPage(member['resource'])

        for f in data.get('files', []):
            fileData = getFileData(f)
            if fileData['language'] == language:
                files.append({
                    'uri' : f['resource'],
                    'data': fileData
                })

        for d in data.get('folders', []):
            files += extractFilesFromFolder(d, language)


    except Exception as e:
        print 'Problem with ' + str(member)
        print e

    return files

print 'gathering all files'
filesList = []

contributions = loadPage('http://101companies.org/resources/contributions')
#contributions = loadPage('http://localhost/services/discovery/contributions')
for member in contributions['members']:
    filesList += extractFilesFromContribution(member, 'Haskell')
    sys.stdout.write('.')
    sys.stdout.flush()

print '\n\n\nanalyzing contents'
contents = {}
for file in filesList:
    content = file['data']['content']
    if content:
        if not content in contents:
            contents[content] = []
        contents[content].append(file['uri'])

clonesList = []
for c, v in contents.items():
    if len(v) > 1:
        clonesList.append(v)

json.dump(clonesList, open('clones.json', 'wS'), indent=4)