package pe.edu.ulasalle.utest.utils.ClasePaServ;

//package pe.edu.ulasalle.utest.utils;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;


public class BuscadorPublicaciones {

    private ServicioBuscadorGoogleBooks googleBooks;
    
    public List<Publicacion> buscarPublicacionesPorTitulo(String cadenaTitulo) {
        List<Publicacion> lst = new ArrayList<Publicacion>();
        Publicacion pub = null;
        for (int i = 0; i < 10; i++) {
            pub = new Publicacion();
            pub.setTitulo(cadenaTitulo + " " + (i+1));
            pub.setFechaPublicacion(LocalDateTime.now().toString());
            pub.setAutor("Autor " + (i+1));
            lst.add(pub);
        }
        List<Map<String, Object>> lstBooks = googleBooks.buscarPublicacionesPorTitulo(cadenaTitulo);
        for (Map<String, Object> map : lstBooks) {
            pub = new Publicacion();
            pub.setTitulo((String) map.get("title"));
            pub.setFechaPublicacion((String) map.get("publishDate"));
            pub.setAutor((String) map.get("authors"));
            lst.add(pub);
        }
        return lst;
    }

    public ServicioBuscadorGoogleBooks getGoogleBooks() {
        return googleBooks;
    }

    public void setGoogleBooks(ServicioBuscadorGoogleBooks googleBooks) {
        this.googleBooks = googleBooks;
    }

    
}