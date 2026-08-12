# Reunión: Evolución de la Fábrica de Software con IA

Resumen

### Elementos de Acción

- [ ]  Corregir la gestión de repositorios: la fábrica debe crear un repositorio separado por cada proyecto generado, no usar el repositorio de la propia fábrica
- [ ]  Eliminar los repositorios de prueba existentes que fueron creados durante las pruebas
- [ ]  Instalar y dejar corriendo localmente un servicio de PostgreSQL dedicado exclusivamente a los proyectos generados por la fábrica
- [ ]  Configurar la fábrica para que conozca las credenciales de conexión al servidor de PostgreSQL local
- [ ]  Agregar un agente especializado en base de datos al grafo de agentes, que se active solo cuando la petición involucre base de datos
- [ ]  Actualizar el stack tecnológico de los agentes: backend con **NestJS** (Node.js + TypeScript) y frontend con **Next.js** más la librería de componentes **Shadcn**
- [ ]  Integrar los archivos de habilidades de [**skills.sh**](http://skills.sh) a los agentes correspondientes para mejorar la calidad del código generado
- [ ]  Implementar la capacidad de que la fábrica trabaje sobre un proyecto existente: al indicarle el proyecto, debe revisar el estado actual antes de continuar, en lugar de crear un repositorio nuevo
- [ ]  Avisar cuando los cambios estén listos para iniciar pruebas más avanzadas

---

### Contexto General

- La reunión trata sobre la evolución de una **fábrica de software basada en IA** que genera proyectos de código automáticamente mediante agentes
- Se revisó el estado actual de la fábrica, se identificaron mejoras necesarias y se asignaron tareas de evolución

### Gestión de Repositorios

- Actualmente la fábrica está dejando el código generado en el mismo repositorio de la fábrica, lo cual es incorrecto
- La fábrica debe crear un repositorio propio por cada proyecto que genere
- Si se le pide una mejora sobre un proyecto ya existente, la fábrica **no debe crear un repositorio nuevo**, sino actualizar el mismo repositorio

### Integración con Base de Datos (PostgreSQL)

- La fábrica actualmente solo genera código básico; se requiere que también pueda construir y desplegar modelos de datos en una base de datos
- El servidor de PostgreSQL local será exclusivo para los proyectos generados por la fábrica, no para la fábrica en sí misma
- La fábrica debe conocer las credenciales de conexión y saber cuándo es necesario involucrar al agente de base de datos según la petición del usuario

### Stack Tecnológico Confirmado

- **Backend:** NestJS (Node.js + TypeScript)
- **Frontend:** Next.js
- **Librería de componentes UI:** Shadcn
- Se confirmó que **Prisma** no está instalado actualmente

### Integración de Skills para Agentes

- Se presentó el recurso [**skills.sh**](http://skills.sh), que contiene archivos `.md` con mejores prácticas y guías detalladas para trabajar con tecnologías específicas como Next.js
- La idea es que los agentes de la fábrica incorporen estas habilidades para producir código de mayor calidad y precisión
- Se debe evaluar si la solución es cargar estos archivos en el RAG u otro mecanismo de integración

### Demo de Aplicación Generada

- Se intentó correr la aplicación de **lista de tareas** generada por la fábrica como prueba
- Hubo problemas de puerto (el puerto 3001 estaba ocupado); se resolvió ejecutando el frontend y backend en el orden correcto
- La aplicación funcionó correctamente: se pudo agregar elementos a la lista
- Se confirmó que la prueba demuestra que la fábrica sí genera aplicaciones funcionales

Notas

Transcripción

Y ahí está el código como tal de la fábrica, eso está bien, ¿sí? Sin embargo, cuando la fábrica se ejecuta y crea un desarrollo, ella deja el resultado en el repositorio, ¿verdad? Sí. Bueno, este repositorio no debe ser este, ¿sí? Porque acá veo que aquí dice APPS en las pruebas 005, que es la prueba que ejecutó. Claro, yo lo uní para yo tener, para hacer la prueba. Pero no se puede borrar, claro.

Sí, pero la idea es que la fábrica, uno es el repositorio de la fábrica, que es lo que ya tienes aquí, ¿sí? Sí. Y aparte tienes que... Debe quedar programado que ella, digamos, bueno yo no sé cómo hacer, pero la idea es que cuando ejecute un encargo, ella misma cree un repositorio y deje ahí el código, ¿sí?

Sí, pero también ella debe saber que de repente si yo le pido algo sobre algo que ya está, no debe crear un repositorio nuevo, sino que debe actualizar el mismo. Por ejemplo, yo le pedimos acá a una calculadora, y listo, me queda un repositor y ahí está. Después le decimos, ah bueno, a ese proyecto de una calculadora, ahora haga, no sé, una funcionalidad de que sea científica.

Ella, la fábrica, no debe de crear un nuevo repositorio, es sobre el mismo, ¿sí? Yo me imagino que él mismo sabe, porque está usando lo mismo que usó para la calculadora en este ejemplo. Y el relaciona y lo une. Tienes que asegurarte lo que me refieras. Bueno.

Esos otros de prueba los voy a borrar, ya los voy a borrar. Porque aquí lo que vamos a hacer es probar.

Sí. Entonces... Bueno, esto es lo primero para que cuando la ejecutemos no toque este repositorio y ya créase para las fábricas. Está bien.

Lo otro es que vamos a comenzar a pedirle cosas que tienen que ver con terricopase de datos. ¿Sí? Sí.

Entonces tienes que hacer lo siguiente, tienes que... Pero si si estás anotando O estás grabando, o grabas la reunión Estoy grabando, pero no en... Ok, pero está grabando lo que estoy diciendo, ¿sí? Sí. Ok. Después de arreglar esto del repositorio... Y lo que tienen que, digamos que, entregar por la IA, es que necesitamos que la...

Esta fábrica genera desarrollos donde también trabaja con baseados pobres. ¿Sí? Es decir, donde en el paquete pues tienen que construir una base de datos, tienen que... desplegarla en un servidor congress, luego el backend, si es una API tiene que integrarla con esa base de datos, o sea que haga todo, porque creo que este primer ejemplo era muy básico, pero ya se.

Yendo más a la realidad. Tiene que ser así, entonces... Yo lo que me imagino... Es que... Tú... Todo eso se lo van a pedir a la IA, claro. Que tú tengas un... Servicio de postres... Corriendo en tu máquina, ¿sí? Sí. Y ese servicio es el que vamos a usar como...

Para toda la fábrica. O sea, es un servicio no para la fábrica como los POSG que se enreda alternativamente. Es un servicio para los productos que genera la fábrica. ¿Sí? Sí.

Ya, eso es.

Ajá, solo. Entonces, en tu máquina vas a tener instalado, corriendo un potoker, un servicio de postgres, pero ese servicio va a ser solo para los proyectos en la fábrica, Si, solo para base de datos hay de prueba, entonces si lo que uno le pide a la fábrica y coloca en una base de datos, el ya debe tener en la información las credenciales como conectarse.

Entonces, resumiendote, lo que tienes que verificar es que tú crees que puedas tener un servicio de pobres corriendo, segundo que la fábrica lo conozca y sepa cómo conectarse. y luego que le pregunte si es necesario un agente especializado en base de datos que yo me imaginaría porque eso de repente cambia

el grafo, porque tiene que tener en cuenta que puede ser, o sea si la petición no involucra a nada, pues no llama a esa gente, pero si sí lo involucra tiene que llamarlo y que cree el modelo. Entonces la idea es que la fábrica, así como desarrolla el código, también cree el modelo de datos, lo borra en la base de datos, y es para que pueda interactuar con los datos.

¿Sí? ¿Me entiendes? Sí Ok, eso sería ya una evolución Muéstrame, ¿puedes compartirme la aplicación que creó? Ay, la mierda ¿Y dijiste que correste loca?

Sí, ya, un momento para correr aquí. Me falta correr el front y ya. Y que ayer sí estaba activado. Sí, está bien. Qué raro.

Y solo confirma, la fábrica está preparada para una cierta pila de baqueritos, ¿verdad?

Usted dice... La pila tecnológica, el stack, los dispajes que va a usar para programar. Si yo sepa, sí. Confírmame si el... ...el baquén es... ...node con el frango ornesto. ¿Ese?

Aquí me dice que el paquete corre con NODJS, pero el código fuente está escrito en Timescript. Claro, claro, pero pregúntale si está usando el framework NESDJS.

O sea, pregúntale como el framework, no lo que la fábrica dice, sino los agentes de la fábrica intentan saberlo. ¿Tienen algún stack específico? ¿Una pila específica de desarrollo?

Los agentes generan código NEST para el backend.

Así, configurada con pila de tecnología, de tecnología.

Hola, para el baque NEST, ¿sí? Sí, NEST, N-E-S-T, J-E-S Y el front, pregúntale por qué... es tan tecnológico que empila, bueno, está trabajando los agentes del front. Next, Boto Jutais. Ok, pregúntale si usa PayPay

¿Sí? ¿Y qué tal va el trío aquí?

Así, si el tron también usa eso.

No, no lo tiene instalado.

Ok, entonces, bueno, así que, a verificar eso. Ahorita está, ahora está corriendo, ya, ya, está corriendo.

No funciona como ayer. Ayer sí había aparecido arriba una aplicación sin estilos de la lista de tareas. Ahorita que intento correrla no... ¿Cómo lo estás intentando correr? En la terminal corro el front y el back, el taquet. Y él ya me lanza un localhost y ahí lo abro y debería verse. ¿Y cuál te agarró? ¿Los dos? ¿O el parquero? ¿Qué?

Mirenlo

El baquete. Pero es que se interrumpe aquí. No queda correcto. No queda sin presión.

Compárteme en pantalla.

Ya que mando un error ahí, ya le comparto.

Sí, está bien. Sí. No sé qué mostrarle. Bueno, el terminal, ¿no? Sí. A ver, esta es... Esta es el barquero. Pero hay un error. Acá, en contra del comando. ¿Cuál es?

Este... Se me olvida como... Tiene un teléfono que toma los borros, no? Si En el PMRD Si, y con gorro Este es el front

Abre, ah bueno, ahí está el editor, entra dentro del proyecto de... Ahí, en la carpeta de APS.

Prueba 07, ¿Entra para qué?

Entra a ese que dice PackKey Él ahí tiene cerca 10 scripts si esos son los comandos que usa creo que uno le da npm run start o sea si es que dice start Eso si, eso es que primero uno coloca NPM root y el comando start, entonces se debe de arrancar, entonces abre el terminal.

Ya estás en el parqueo NPM Rolestar

Ahí están diciendo... Ya vas. Aún no he escuchado el galope nativo. Ya vas. Para hablárselo a mí. Ya descanse.

Mateo, tú no conectas, no estás descalzo conectando eso.

A ver que está diciendo ahí...

Ah, que ya está en uso ese puerto, el puerto 3001, entonces abre el navegador. Pero es el grafana, no es el propio. El grafana está en el 3.000, ¿no? Sí. Por eso... Yo lo activo en el 3.2 Abre el código otra vez El código...

¿Cuál? Estoy confundida El editor, eso El Es el terminal, el código es eso

Por acá no está el puerto, hay una parte donde...

Abre el otro .tsconf Otro archivo

que vuelve a terminar.

Dale otra vez en el PMRUNESTAR y le das espacio.

espacio, creo que coloca el guion, guion V8, V8 support espacio, 3200

¡Gracias por ver el video!

Si viene pregunta la IA me soluciona ese problema. Sí, sí, dile que te corra, no, que corra el baquete y el fronero, no lo entiendo, para probarlo tú en el aviador. Sí.

Pero usted me interrumpo del front, que le hagan los dos. Ah, es que el front ya está en el 3001. Pues era el 3001. No, pero mira, ahí está corriendo el tremilo, ¿no?

Y en otra pestaña a la izquierda.

Esa es la que está... No, ya va. Abre la boca. Dale Ctrl C. Yo creo que el backend está fijo para que corra en el 3.1, en la otra pestaña vuelve a ejecutarlo, pero solo en el PMRUN está.

Un saludo y hasta la próxima.

Yo creo que es alternar. Eso es porque, ¿sí ves? El baquete está fijo para el 3001. Entonces, como el otro ya lo ocupaba... Entonces, el orden es este. Ahora sí ejecuta este. En el PM de Rundell.

Si, este si esta automático, agarra el entro del puerto que este libre. Ahora si abre el localhost 3.2.

Ya arrancaron, ya no están en la roca.

Ok, y agrega aceite.

¿Qué agrego acá? Pruebalo, o sea, pruebalo, coloca lo que sea ahí y dale a agregarlo.

Bueno, sí funciona. ¿Esto no lo habías hecho? No. Ay, sorry. Bien, lo que necesitamos ahorita es probar que la fábrica realmente funciona, ¿sí? Sí. Que me creo esto, pero la prueba ya desplegó y funciona, ¿no? Que esos botones sirvan, ¿sí? Claro. Claro, sí.

Entonces, ya bueno, hasta aquí estará mi clase. Ahora, enfoquémosla en esto que te voy a decir. Primero... Ya.

¿Estás grabando o no estás o cómo?

Eh, yo no se me ocurrió al principio grabar en Notion y se me vino olvidando aquí al tarde No me acuerdo ni como se hace eso Entonces estoy grabando en otro lado Ya, yo reviso eso, ya estoy grabando acá Bueno, primero tenemos que lograr que la fábrica esté preparada para trabajar.

con base de datos pobres si que el baque pueda trabajar con base de datos pobres entonces como es, la fabrica debe tener ya disponible un servidor corriente no es que la fabrica va a crear un servidor si sino ella va a saber, yo tengo disponible esta conexión donde puedo crear vacidad y puedo correr todo lo que necesite entonces por eso tiene que tener local un servidor pobre corriendo

Y luego, la fábrica debe poder saber eso, o sea los agentes, mejor dicho, debe, no sé si pongan variables de entorno, debe tener la... la conexión a esa base de datos y el grafo como tal, los agentes tienen que estar preparados para si lo que se le pide con base de datos que haya un agente que se encargue de eso, un agente especializado en base de datos.

Sí. Eso supongo que cambia el grafo y eso, pero por eso digo que al menos eso sí, que la actividad fótica se adapte a eso, ¿sí?

Luego, lo otro que tienes que hacer es decirle a... digamos que el parquete...

Pues ya está simple, igual te lo explico acá, el nuevo de JS y el framework es JS, ¿sí? Sí. ¿Y el front?

y los componentes de la librería Sade Sena, ¿sí? O sea, tú tienes que decirle, digamos que los agentes del Bakken sean especialistas en esa tecnología y los del Throne en esta otra, ¿sí? Sí. Luego, hace un link de skills.sh

¿Sí lo ves?

No me está compartiendo. Usted me está hablando... Sí, ahí, en skills.sh Si, si hay luego. Claro, claro. Ya.

Estoy aquí, ¿no? Claro, pero... ¿Ves el link que te mandé? skills.sh Sí, aquí está. Ábrelo.

Esta página es... Tú sabes que los agentes... Hay una... Bueno, hace un tiempo salió esto que son como las habilidades. Entonces, ¿cuál es la utilidad de esto? Que, por ejemplo, si yo quiero que... Si yo voy a hacer un trabajo con Next.js, ¿sí? Sí. Entonces, ya hay habilidades redactadas.

para ese tipo, para trabajar con ese NX-DS, ¿sí? Sí. O sea, eso a la final es un archivo .md donde le detalla bien cuáles son las mejores prácticas y cómo trabaja adecuadamente con esa tecnología, ¿sí? Entonces, lo que tiene que decir la idea es que también la fábrica y los agentes deben tener esta herramienta para que el trabajo lo hagan con una perfección.

Entonces, yo no sé si la solución sea en el rack cargar estos archivos de las habilidades o de qué forma, ¿sí? Claro. Pero que necesitamos integrar estas skills a esos agentes porque ya los agentes les estamos diciendo que trabajan en unas filas especificas.

Sí. Bueno, entonces, esto, me sé, por eso incorporaré esto, ¿sabía? Entonces, el resumen sería los postres. Lo de la pila de front y el back y que trabajen.

Y esta es la tarea que usted me decía en un principio, la estamos retomando hoy.

Como así tarea en un principio. Al inicio de la reunión usted me estuvo explicando que tenía que hacer unas tareas, es esto mismo pero está puesto. Sí, vamos a pulirla. Con esto, pues, y la idea después de esto es sí empezar a correrla e irle pidiendo cosas, ¿sí? Está bien.

Bueno, yo sé que hay otra cosa más. Lo otro es que necesito que cuando la fábrica se ejecute, uno le pueda indicar cuál proyecto es para que sigamos. Que ella no esté creando un repositorio y no viene a ser pagada. Trabajar sobre este proyecto, ¿sí? Sí.

porque es muy diferente. Si uno le indica el proyecto, ella primero tiene que entrar y revisar qué es lo que hay para continuar. En cambio, cuando es desde cero, pues no revisa nada y empieza a programar. Entonces también eso, diles que la fábrica debe estar preparada para eso. Está bien.

Entonces, eso soy. Cuando lo tengas me avisas a ver si empezamos a hacer pruebas. Está bien.

Listo. Bueno, solo gracias por avisarnos. Gracias. Bueno, chao. Chao.

Hola, ¿cómo está? Muy buenos días.