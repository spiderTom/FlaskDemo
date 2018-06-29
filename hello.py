import sys
import os, tempfile, subprocess
from flask import Flask, render_template, redirect, url_for, request

INDEX = 0
TEMP = tempfile.mkdtemp(suffix='_py', prefix='learn_python_')
EXEC = sys.executable

def get_name():
    global INDEX
    INDEX = INDEX + 1
    print("in get_name %d" % INDEX)
    return 'test_%d' % INDEX

def write_py(name, code):
    fpath = os.path.join(TEMP, '%s.py' % name)
    print("in write_py %s" % fpath)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(code)
    print('Code wrote to: %s' % fpath)
    return fpath

def decode(s):
    try:
        return s.decode('utf-8')
    except UnicodeDecodeError:
        return s.decode('gbk')


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run',methods=['GET','POST'])
def testSubmit():
    content = request.form.get('code')
    print("in testSubmit content is %s" % content)
    #return content
    r = dict()

    try:
        fpath = write_py(get_name(), content)
        print('Execute: %s %s' % (EXEC, fpath))
        r['output'] = decode(subprocess.check_output([EXEC, fpath], stderr=subprocess.STDOUT, timeout=5))
    except subprocess.CalledProcessError as e:
        r = dict(error='Exception', output=decode(e.output))
    except subprocess.TimeoutExpired as e:
        r = dict(error='Timeout', output='执行超时')
    except subprocess.CalledProcessError as e:
        r = dict(error='Error', output='执行错误')
    print('Execute done.')
    print(r)
    #self._sendHttpHeader()
    #self._sendHttpBody(r)
    return r['output']


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


