# Planificación de Fábrica de Desarrollo con Agentes IA

Subítem: Plan de Implementación — Fábrica de Desarrollo con Agentes IA (local / validación de grafo) (https://app.notion.com/p/Plan-de-Implementaci-n-F-brica-de-Desarrollo-con-Agentes-IA-local-validaci-n-de-grafo-3878229d6b0d48c28e5590c8f65c6c56?pvs=21)

Resumen

### Elementos de Acción

- [ ]  Sol: usar esta transcripción para pedirle a la IA que cree un documento de plan de implementación detallado en la base de datos de documentos de Notion (misma sección donde está "Fábrica de Encargos"), basándose en lo discutido en esta reunión
- [ ]  Sol: revisar el plan de implementación generado antes de pasarlo a Andrés, y aportar criterio propio sobre si responde a lo solicitado
- [ ]  Sol: si la IA tiene dudas sobre el plan, pasarlas a Andrés
- [ ]  Andrés: revisar el plan de implementación y dar indicaciones para comenzar la implementación siguiendo la metodología del equipo
- [ ]  Andrés: compartir el token de OpenRouter con Sol para configurar los agentes
- [ ]  Verificar que Sol tenga acceso al espacio **ADN Fábrica Lab** en GitHub

---

### Objetivo General

- La tarea consiste en construir una **fábrica de desarrollo** (software factory con agentes IA) de forma local, como evolución del modelo ya existente de "Fábrica de Encargos"
- El objetivo **no es producción**, sino **validar el grafo de agentes**: qué agentes son necesarios, cómo se comunican y cómo funciona el flujo
- Una vez validado el grafo, se extraerá el código del mismo para la versión productiva

---

### Referencia Base

- Usar el documento **"Fábrica de Encargos - Plan de Implementación v2"** como referencia para que la IA construya un plan similar orientado a una fábrica de desarrollo
- El plan debe incluir: flujo de la fábrica, agentes involucrados, estrategia de escritura de código, y configuración del RAG

---

### Stack Tecnológico

- **Backend:** NestJS (framework de backend)
- **Frontend:** NextJS
- **Base de datos:** PostgreSQL local en contenedor
- **Vector store (RAG):** Qdrant, también en contenedor
- **Modelos IA:** OpenRouter — cada agente tendrá asignado un modelo específico

---

### Infraestructura y Despliegue Local

- Todo debe correr en la máquina de Sol usando **contenedores Docker** (nada instalado directamente en la máquina)
- La fábrica debe conectarse a la organización **ADN Fábrica Lab** en GitHub para crear y gestionar repositorios por proyecto
- El código generado debe subirse a ramas, con aprobación humana antes de mergear

---

### Intervención Humana

- Los checkpoints del grafo que requieran intervención humana se manejarán **por terminal** (no por Slack)

---

### RAG - Conocimiento de los Agentes

- Se debe evaluar qué información cargar en Qdrant: posiblemente documentación de las tecnologías usadas
- El plan de implementación debe indicar si es necesario pre-cargar el RAG antes de ejecutar la fábrica

---

### Estrategia de Escritura de Código

- El plan debe definir la estrategia óptima para que los agentes escriban código en proyectos de múltiples archivos, tanto pequeños como grandes: si escriben directo al repositorio o en memoria

---

### Modelos IA y Límites

- Nokia (Claude) está comenzando a limitar el uso a partir de hoy
- Si hay problemas de créditos con Claude, intentar con **GPT-4.5/4o** o **Gemini 2.5** como alternativas

---

### Próximos Pasos

- El primer paso concreto es generar el plan de implementación usando esta transcripción
- Andrés estará atento al avance y dará indicaciones para comenzar la implementación una vez aprobado el plan
- Se estima que es una tarea larga que puede tomar más de una semana entre construcción e iteración

Notas

Transcripción

Cuando termines, le pones el título que intereses, le pones al título de esa nota, como el título de la redacción. Sí, ya está. Bueno, Sol, mira, te voy a explicar entonces lo que yo necesito que hagas. Tú sabes que ahorita en Nokia hemos venido registrando...

Lo que estamos haciendo con las fábricas, ¿sí? Sí Digamos que... a ver... En el espacio de ADN... quizás... Hay una sección de documentos

Y ahí, hay una que dice fábrica de cargos e internamente está el plan de implementación, ¿sí? Bueno, ese es uno que hicimos, ¿sí? Ahora, bien, yo ahorita estoy haciendo, como te expliqué, la evolución de esto, ¿sí?, para... de una forma más genérica para que podamos tener varias fábricas, bueno, varias cosas, ¿sí? Sí

Yo lo que he estado pensando, es que ahorita esto que yo voy a, ya no es algo, esto es lo que voy a hacer, lo tengo que hacer yo, entonces... pensando en la idea que tu avances relacionada con lo que estamos haciendo que vayas haciendo cosas relacionadas con la IA entonces lo que estaba pensando era asignarte una tarea no es corta, es larga

Y es que tú construyes una fábrica de desarrollo, ¿sí? Ajá. Y digamos que la idea es que eso lo construyas, o sea, por ejemplo, tú le puedes pedirle, o incluso estas transcripciones están bien para eso, para que sea más fácil. sepa mas o menos lo que tienes que hacer por eso te digo acá el documento en fábrica de encargos, plan de implementación ahí esta como todo lo que se hizo con la fábrica de encargos si ahora la versión 1 o la 2

ahora lo que tendría que hacer es crear una fábrica ¿De desarrollo de sombra? ¿Sí? ¡Sí!

Esa fábrica la vas a hacer local, o sea, todo va a correr en tu máquina, ¿sí? Sí.

todo va a correr en tu maquina y la idea es que tú primero le pidas a la IA que te Digamos que lo puedes decir basando en este plan de implementación de fábrica de encargos versión 2. Ahora yo quiero implementar uno similar para una fábrica de salud de los ojos. Dile que vas a hacerlo desde cero. Porque vas a instalar un local en tu máquina y ahí no hay nada instalado. Claro. Que te cree un plan de implementación para eso. En ese plan te debe indicar cómo va a ser el flujo de esa fábrica.

Sí, lo que es el grafo. Sí. Entonces, para que nosotros antes, o sea, ese plan de implementación, todo lo que va a tener, hay una parte donde debe decirnos cómo va a ser el flujo. para que esta fábrica funcione, o sea, cuáles son los agentes que va a tener, ¿sí? Claro.

Osea, la idea, porque, que pasa, después que yo termine todo esto, esa es la que hay que escoger. Entonces, yo quisiera que tú construyeras una y que lo importante, lo importante que vamos a sacar de valor de ahí. Es el grafo, porque el grafo tiene los agentes, o sea, es pulir eso, porque digamos que, yo sé que tiene que haber un arquitecto de software, tiene que haber un programador, sí, pero...

digamos que se construye el gramo y se afine de manera que cuando ya llegue yo a ese punto ya tengamos como que algo ya recorrido y cómo va a funcionar esa fábrica de desarrollo ¿Sí? Sí Entonces, muy importante todo esto que estás transcribiendo, se lo pasas a la A&E, esto es lo que pidieron hacer prácticamente, no tienes que hacer enseñanzas y ver nada, ella lee esto y ya saben que hay que hacer, ¿sí? Sí. Entonces, eh...

Lo que yo espero es que esa implementación que vas a hacer, lo importante es validar. y digamos que podamos tener un gráfico con los agentes y pues con las pruebas que le hagamos irlo cubriendo. Eso es lo más importante, no tanto de que si... Vamos a tener, o sea, no sé, digamos que eso no va a ser para producción, eso es solamente para validar el grafo, después lo que vamos a agarrar de ahí es como tal el código del grafo y los agentes, ¿sí? Sí Entonces, esto...

Otra cosa importante es que esa fábrica por ahora va a ser para desarrollar software con NXJS que es un framework, NXSTJS que es un framework de backend Y para el front, NXTS que es NXSTJS Esto también para el front, deberíamos tener, o sea, debería trabajar con...

Porque esa fábrica pues ya tiene que venir, como, configurar los agentes con esas habilidades, ¿sí? Sí. Entonces debemos, esa fábrica debe tener especialistas en el back-end con esas tecnologías y los drones, ¿sí? Sí. para base de datos tiene que ser base de datos públicos y igual, si de repente también la fábrica necesita conectarse o tener acceso a una base de datos puede que sea una base de datos local, de tu máquina en un contenedor

Otra característica es que todo lo que vas a hacer local lo hagas en contenedores, que no sale nada en tu máquina, así todo se va acabando. Los doques, los tenedores, ¿sí? Sí Y... ¿qué otra cosa? A ver...

No, respecto a la intervención humana, ¿sí?, porque ese grafo va a tener checkpoints. Claro. Yo lo conectaba con Slack. Yo creo que es sencillo ponerla. Cuando yo lo hice me pareció sencillo. Hay unas instrucciones donde uno tegra...

¿O no? ¿Sabes que no? Es que como están de pruebas son... Que si la fábrica requiere intervención con el humano, que lo haga a través del terminal, ¿sí? Ah, bueno. Sí. Y así en la pantalla negra, igual como ahí ejecutan los comandos, pues que ahí pida las cosas.

Sí. ¿Sí? Esto... Luego... Esa fabrica... Tiene que... Digamos... Ir... O sea, la fábrica a medida que va esperando, o sea, va pasando por los agentes, ellos van inscribiendo códigos, ¿sí? Y a la final, ese código lo deben subir a un repositorio. ¿Sí? Sí ¿Tú tienes acceso, déjame ver? Al mío Al suyo no Porque eso es con unas claves

para comprobar

Si, si, si.

Te envié una invitación a un espacio que se llama Adelie Fábrica Lab, ¿sí? Sí. Ahí tú puedes crear repositorios. Ese es un espacio de pruebas, ¿sí? Ahí no hay ningún repositorio real que estemos usando, ¿sí? Está bien. Entonces, tú tienes que... Esta fábrica tiene que conectarse con este espacio de...

con esta organización adn fábrica lab y que ella cree los repositorios vino que va a crear un repositorio por proyecto, no se, entonces eso tiene que definirse Imagino que uno le tiene que indicar al comienzo en que proyecto va a trabajar, porque no necesariamente uno la pone a funcionar por proyecto, sino que yo la pongo a funcionar para agregar solo una funcionalidad, algo que ya está en un repositorio, entonces no es que siempre agarre y cree un repositorio, es lo que me refiero, desde el comienzo uno, todo el contrato que se le pasa al comienzo, debería tener, indicárseles, no sé, el repositorio.

Y seguramente esta fábrica va a necesitar una base de agua pobre, lo mismo que teníamos hace rato, que sea local, ¿sí? que aún se creen un contenido local en su maquina. Agit, ¿no? Sí, en Sol Celote le envié la invitación. La única que tengo es de WP Control, del 20 de mayo.

Voy a quitar eso. Pero no, no veo. ¿No te ha llegado? Creo que no. No, pero, no, entra aquí, a tu puesta de aquí. Acá debe haber una parte donde tienes la indicación de este agente.

todo lo que hace, lo pongo en una rama, una estrategia, porque obviamente no va a poner de una rama ahí, sino que habrá una aprobación humana y esa aprobación es la que me manda a probar el código, ¿sí? Sí. Esto... Luego hay otra cosa importante, bueno, todo como queda grabado, importante para la planificación, y es la forma como va a ir escribiendo el código, o como lo va a ir leyendo, o sea, puede...

Como es desarrollo, el proyecto puede ser con muchos archivos, muy grandes, entonces yo no sé internamente cuando va iterando, cuando va pasando en el grafo con los diferentes agentes, o sea es posible que haya un agente del front. y después otro de Backend, y otro que también trabaje con el Backend y cada uno va a ir escribiendo código entonces, yo no sé, ahí en la planificación, que se recomienda cuál es la estrategia más óptima para ir escribiendo código sí o sea, si irlo escribiendo directo en el repositorio y hacerle códigos o lo tiene en memoria, ¿sí?

¿y cuál es la forma más óptima? para que esto realmente funcione para proyectos pequeños y proyectos grandes. ¿Sí? Sí. Y bueno, yo creo que en general es eso. Es una fábrica de desarrollo que vas a juntar local. No necesita, o sea, debe ser como lo más...

A veces me enredo en lo que te voy a decir, pero lo que necesitamos es definir esa fábrica. Vamos a afinar el grafo, ¿sí? Sí. los agentes y eso es lo que nos vamos a sacar para la que va a estar en producción, que no va a tener nada que ver con lo que tienen instalado ahí, ¿sí? También es importante que esa fábrica va a comunicarse con un RAC, ¿sí?

Sí. ¿Será que va a estar en un Q-drant, un aseato de vectores que se llama Q-drant? O sea, también se instalaría en un contenedor, ¿sí? Sí. Y ahí, digamos, que sí es bueno que deba tener cargada... O sea, que también sugiera que información debe tener cargado los agentes.

O sea, no información de la empresa, sino de... No sé si sea necesaria información de las tecnologías, qué sé yo, ¿sí? que en la modificación nos diga si es necesario que previamente el rack lo tengamos cargado porque la idea es que los agentes consulten el rack para que le puedan dar más contexto.

Entonces, igual el primer paso es que con esta grabación tú le indiques que en Nokia En la base de datos de documentos, ahí mismo donde está fábrica de encargos, cree un nuevo documento

bueno lo que debes hacer es

Yo te dije que esto lo creamos dentro de notas, ¿verdad? Sí, de privado. Sí, no, igual, entonces que ahí mismo, como un subtítulo... Es el que cree un documento para implementar lo que se está pidiendo en esta reunión. Y eso hazlo con Facebook, Zinko y que sea muy detallado.

Está bien. Entonces, y que... Si tiene dudas, te haga preguntas. Simplemente te va a hacer preguntas y me las... Si tiene dudas, me las pasa. Sí. Sí. Sí. Sí. Sí. Sí.

En cuanto, claro, cuando esté ese plan de implementación, primero lo lee, ojea, o no sé, aporta un criterio ahí, si creen que quedó bien a lo que les estoy pidiendo, ¿sí? Lo que digo es que le des como una revisión inicial, no me lo pases una vez a mí, ¿sí? Claro. Y después si yo lo reviso y si se ajusta algo, bueno, si no, ahí tú empiezas y yo ya te indicaría cómo vas a empezar a implementarlo, ¿sí? Para que sigas como la metodología que yo voy siguiendo.

Esta bien. Esto es una tarea larga. Me imagino. Si, entonces tienes que estar bien dedicada y para ver, no sé si esta semana sale. Porque, o sea, uno es construirla y lo otro después es iterarla. Otra cosa importante es que los agentes se van a utilizar Open Routers, ¿sí?

Yo ya tengo una cuenta ahí, te pasaría un token, pero esto es importante porque eso es lo que tienen que configurar los agentes para que se conecten con los modelos, ¿sí? Sí. Y otra característica importante es que cada agente se le asigna un modelo, ¿sí?

de cada gente uno le puede definir qué modelo paten va a usar, modelo de hierro

Sí.

Creo que... Creo que eso sería solo. Está bien.

Y Nokia dice que desde hoy ya está limitando el uso, ya no es como antes que casi que no nos ponía límites. Entonces esto... ¿Eso es una actualización? Sí, ya avisaron que a día de hoy van a poner el comunismo. Entonces, si de repente con el Facebook te da un problema, digamos llego un punto en que ya no tienes créditos, tienes que intentar con otros modelos, intenta con los de GPT, no sé, los altos, 5.6, 5.5, ¿sí? Sí.

Y si no, intenta con él. Hay uno que dice química 3.

Está bien. Si está de química 3. Pues eso sería suerte.

¿Sí? Sí, y ahorita mismo comienzo. Bueno, está bien. Ahorita yo estoy atento entonces. Gracias. Bueno, esto es gracias a ti. Hablamos. Muy bien. Chao. Chao.