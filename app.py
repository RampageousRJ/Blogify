from blogify import app,db
from flask_migrate import Migrate

migrate = Migrate(app,db)

if __name__=='__main__':
    app.run(debug=True)
    
''' cd 'E:\Study\OneDrive - Manipal Academy of Higher Education\Coding\Mini-Projects\Blogify'
    source virt/Scripts/activate                                                                '''