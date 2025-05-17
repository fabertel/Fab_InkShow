
17/05/25
- LOGIN ADMIN SICURO (ma che non serve per ora! aggiornamento gallry si fa da backend ) 
- disabled price con #modal-price {display: none;} in CSS 
= added second gallery e dynamic gallery 
- utils e processo per creare new galleries 
= added gallery title in megalleries_meta.json adata 
= added privacy and SEO optimization 

ADMIN LOGIN
http://localhost:8000/page?md=admin&token=jU5fXcOHrgjmtEZ4G8JaNJaf6Sd34tSFeiAZfYLFYuTI


COME CREARE ALTRE GALLERIE
    metti foto in subfodler IMAGES 
    usa UT1_generate_gallery_xlsx.py per fare XLS 
    finalizza XLS 
    lancia UT2_Create_Thumbnails.py
    lancia UT3_xls_to_json.py cambiando filenames 
    salva nuovo file JSON in static/, ad esempio data_animali.json.
    Aggiungi un link a /gallery/animali e FastAPI caricherà automaticamente gallery.html e data_animali.json.


