Visual Studio Code
1. Crear una carpeta exclusivamente para el proyecto actual
2. Añadir esa carpeta al Área de Trabajo de VSC
3. Crear un archivo con el nombre de ".gitignore"
    En el archivo .gitignore contiene los directorios o nombres de archivos que Git debe ignorar, no se subiran al repositorio. Si es un archivo importante, se debe aclarar en el README.md, o un archivo de texto "Para su funcionamiento, crear un archivo de configuración"
4. Palabras reservadas en comentarios
    //TODO: tareas que quedan por hacer
    //FIXME: como una tarea, pero más específico, arreglar, corregir una función
    //HACK: una solución temporaria, un parche, hay que mejorarla más adelante
    //NOTE: para destacar el comentario de una función, e.g.: 'parece que no hace nada, no borrar, es para mantener compatilidad con versiones anteriores'
    //BUG: para comentar un bug (falla) que se encontró (y hay que solucionarla en algún momento)
    //OPTIMIZE: cuando una función parecería ser muy compleja, y habría que revisarla para ver si se puede optimizar
    //WARNING: para advertir que esa parte del código, puede dañar el funcionamiento completo de la aplicación


GitHub
1. Crear una cuenta en github.com
   -En la esquina derecha, hacer clic en "+" y seleccionar "New Repository"
   -Configurar el repositorio:
   -Repository Name: Nombre del repositorio (nombre del proyecto)
   -Description: Descripción del proyecto, ¿qué hace?
   -Public / Private: si es visible para todos o no
   -README.md: es un archivo de ayuda, instrucciones si el proyecto necesita una configuración previa, como una base de datos precargada, plugin instalados, etc
   -Create repository
2. Subir nuestro proyecto a GitHub
    -Desde la terminal, hay que ir hasta la carpeta del proyecto:
            cd proyectos/curso-python/entrega-final
    -desde esa terminal, ejecutar los comandos de git
        -Inicializar git
            git init
        -Agregar todos los archivos que hay en la carpeta
            git add .
        -Comentar que estoy haciendo
            git commit -m "Primera versión del proyecto"

    -Vincular la carpeta local del proyecto, con el repositorio de Github
        -Copiar la url del repositorio
            https://github.com/tu-usuario/proyecto.git
    -En la terminal donde estabamos, lo vinculamos:
            git remote add origin https://github.com/tu-usuario/proyecto.git
    -Subir los archivos a github
            git push -u origin master
3. Gitignore. Si se el proyecto se subió, y después se crea el archivo .gitignore, hay que hacer estos pasos
        git rm -r --cached .
        git add .
        git commit -m "Se agrega .gitignore"
        git push
4. Actualizar proyecto. Para subir las modificaciones, actualizaciones:
    git status
    git add .   /  git add nombre-archivo
    git commit -m "Comentario sobre los cambios hechos"
    git push
5. Actualizar por fuerza (bruta)
    En el paso 4, en vez de escribir 'git push', escribimos:
        git push --force
6. Actualizar con problemas
    git pull origin master ('master' es el nombre de la rama, puede ser otro)
    git add archivo-que-molesta
    git commit -m "Se volvió a subir el archivo XXYY que causaba problemas"
    git push / git push --force

GitHub - Clonación y Ramas