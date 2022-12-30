# Test Data Dictionary

This document describes the organized data collected during the blind test of the research. 
This data was collected from a population of 117 participants around the world through the platform SurveyMonkey. The blind test was done in three languages, being Portuguese, English and French. The participants of the test were asked to listen to five music excerpts containing 4 samples generated by AI and the remaining one played and composed by a human. The test subjects were responsible to answer a series of questions about the samples (check list below).

You can find the csv file with all the responses at [test-results/all-responses.csv](all-responses.csv).

> Note: The data available in the csv file was reduced exclusively to the answers of the questions in order to protect the identity of the participants.


## Sample 1 - Music Transformers

- q1:
  - **Labels**:
    - De 0 a 10, quão musical você acha que essa música é? Trecho Musical 1
    - How musical do you think this piece of music is? Sample 1
    - À quel point pensez-vous que ce morceau de musique est musical? Extrait musical 1
  - **Values**:
    - [0-10]
- q2:
  - **Labels**:
    - Você acredita que essa música foi feita por um humano ou um computador?
    - Do you believe this song was made by a human or a machine?
    - Croyez-vous que cette chanson a été faite par un humain ou une machine ?
  - **Values**:
    - [0, 1] (0: humano/human/humaine, 1: computador/machine)
- q3:
  - **Labels**:
    - Você diria que o trecho musical ouvido se assemelha a músicas do gênero clássico? (música clássica)
    - Would you say that the musical excerpt heard resembles songs of the classical genre? (classic music)
    - Diriez-vous que l'extrait musical entendu ressemble à des chansons du genre classique ? (musique classique)
  - **Values**:
    - [0, 1] (0: não/no/non, 1: sim/yes/oui)
  
- q4:
  - **Labels**:
    - (Opcional) Adicione quaisquer considerações que você possa ter sobre ao trecho 1
    - (Optional) Add any considerations you might have regarding sample 1
    - (Facultatif) Ajoutez toutes les considérations que vous pourriez avoir concernant l'extrait musical 1
  - **Values**:
    - [text or null]

## Sample 2 - Performance RNN
- q5:
  - **Labels**:
      - De 0 a 10, quão musical você acha que essa música é? Trecho Musical 2
      - How musical do you think this piece of music is? Sample 2
      - À quel point pensez-vous que ce morceau de musique est musical? Extrait musical 2
  - **Values**:
    - [0-10]
  
- q6:
  - **Labels**:
    - Você acredita que essa música foi feita por um humano ou um computador?
    - Do you believe this song was made by a human or a machine?
    - Croyez-vous que cette chanson a été faite par un humain ou une machine ?
  - **Values**:
    - [0, 1] (0: humano/human/humaine, 1: computador/machine)
  
- q7:
  - **Labels**:
    - Você diria que o trecho musical ouvido se assemelha a músicas do gênero clássico? (música clássica)
    - Would you say that the musical excerpt heard resembles songs of the classical genre? (classic music)
    - Diriez-vous que l'extrait musical entendu ressemble à des chansons du genre classique ? (musique classique)
  - **Values**:
    - [0, 1] (0: não/no/non, 1: sim/yes/oui)
  
- q8:
  - **Labels**:
    - (Opcional) Adicione quaisquer considerações que você possa ter sobre ao trecho 2
    - (Optional) Add any considerations you might have regarding sample 2
    - (Facultatif) Ajoutez toutes les considérations que vous pourriez avoir concernant l'extrait musical 2
  - **Values**:
    - [text or null]

## Sample 3 - MuseNet
- q9:
  - **Labels**:
    - De 0 a 10, quão musical você acha que essa música é? Trecho Musical 3
    - How musical do you think this piece of music is? Sample 3
    - À quel point pensez-vous que ce morceau de musique est musical? Extrait musical 3
  - **Values**:
    - [0-10]
- q10:
  - **Labels**:
    - Você acredita que essa música foi feita por um humano ou um computador?   
    - Do you believe this song was made by a human or a machine?
    - Croyez-vous que cette chanson a été faite par un humain ou une machine ?
  - **Values**:
    - [0, 1] (0: humano/human/humaine, 1: computador/machine)
  
- q11:
  - **Labels**:
    - Você diria que o trecho musical ouvido se assemelha a músicas do gênero clássico? (música clássica)
    - Would you say that the musical excerpt heard resembles songs of the classical genre? (classic music)
    - Diriez-vous que l'extrait musical entendu ressemble à des chansons du genre classique ? (musique classique)
  - **Values**:
    - [0, 1] (0: não/no/non, 1: sim/yes/oui)
  
- q12:
  - **Labels**:
    - (Opcional) Adicione quaisquer considerações que você possa ter sobre ao trecho 3
    - (Optional) Add any considerations you might have regarding sample 3
    - (Facultatif) Ajoutez toutes les considérations que vous pourriez avoir concernant l'extrait musical 3
  - **Values**:
    - [text or null]

## Sample 4 - Custom GRU
- q13:
  - **Labels**:
    - De 0 a 10, quão musical você acha que essa música é? Trecho Musical 4
    - How musical do you think this piece of music is? Sample 4
    - À quel point pensez-vous que ce morceau de musique est musical? Extrait musical 4
  - **Values**:
    - [0-10]
- q14:
  - **Labels**:
    - Você acredita que essa música foi feita por um humano ou um computador?
    - Do you believe this song was made by a human or a machine?
    - Croyez-vous que cette chanson a été faite par un humain ou une machine ?
  - **Values**:
    - [0, 1] (0: humano/human/humaine, 1: computador/machine)
  
- q15:
  - **Labels**:
    - Você diria que o trecho musical ouvido se assemelha a músicas do gênero clássico? (música clássica)
    - Would you say that the musical excerpt heard resembles songs of the classical genre? (classic music)
    - Diriez-vous que l'extrait musical entendu ressemble à des chansons du genre classique ? (musique classique)
  - **Values**:
    - [0, 1] (0: não/no/non, 1: sim/yes/oui)

- q16:
  - **Labels**:
    - (Opcional) Adicione quaisquer considerações que você possa ter sobre ao trecho 4
    - (Optional) Add any considerations you might have regarding sample 4
    - (Facultatif) Ajoutez toutes les considérations que vous pourriez avoir concernant l'extrait musical 4
  - **Values**:
    - [text or null]


## Sample 5 - Maestro
- q17:
  - **Labels**:
    - De 0 a 10, quão musical você acha que essa música é? Trecho Musical 5
    - How musical do you think this piece of music is? Sample 5
    - À quel point pensez-vous que ce morceau de musique est musical? Extrait musical 5
  - **Values**:
    - [0-10]
- q18:
  - **Labels**:
    - Você acredita que essa música foi feita por um humano ou um computador?
    - Do you believe this song was made by a human or a machine?
    - Croyez-vous que cette chanson a été faite par un humain ou une machine ?
  - **Values**:
    - [0, 1] (0: humano/human/humaine, 1: computador/machine)
  
- q19:
  - **Labels**:
    - Você diria que o trecho musical ouvido se assemelha a músicas do gênero clássico? (música clássica)
    - Would you say that the musical excerpt heard resembles songs of the classical genre? (classic music)
    - Diriez-vous que l'extrait musical entendu ressemble à des chansons du genre classique ? (musique classique)
  - **Values**:
    - [0, 1] (0: não/no/non, 1: sim/yes/oui)
  
- q20:
  - **Labels**:
    - (Opcional) Adicione quaisquer considerações que você possa ter sobre ao trecho 5
    - (Optional) Add any considerations you might have regarding sample 5
    - (Facultatif) Ajoutez toutes les considérations que vous pourriez avoir concernant l'extrait musical 5
  - **Values**:
    - [text or null]

## About you section
- q21:
  - **Labels**:
    - Como você classificaria sua sensibilidade musical?
    - How would you rate your musical sensitivity?
    - Comment évaluez-vous votre sensibilité musicale ?
  - **Values**:
    - [0-10]
  
- q22:
  - **Labels**:
    - Com que frequência você ouve música clássica?
    - How often do you listen to classical music?
    - A quelle fréquence écoutez-vous de la musique classique ?
  - **Values**:
    - [0, 1, 2]
        - 0: ["Eu não escuto música clássica", "I don't listen to classical music","Je n'écoute pas de musique classique"] 
        - 1: ["De vez em quando", "Every now and then", "De temps en temps"]
        - 2: ["Ouço com frequência", "Frequently", "Fréquemment"]
  
- q23:
  - **Labels**:
    - Você tem alguma experiência prática com música?
    - Do you have any practical experience with music?
    - Avez-vous une expérience pratique avec la musique?
  - **Values**:
    - [0, 1, 2, 3, 4]
        - 0: ["Não", "No", "Non"] 
        - 1: ["Sim, consigo fazer música com a minha voz ou com um instrumento musical", "Yes, I can make music with my voice or with a musical instrument", "Oui, je peux faire de la musique avec ma voix ou avec un instrument de musique"]
        - 2: ["Sim, estudo/estudei teoria musical (conservatório, escola de música, autodidata)", "Yes, I study/studied music theory (conservatory, music school, self taught)", "Oui, j'ai étudié la théorie de la musique (conservatoire, école de musique, autodidacte)"]
        - 3: ["Sim, eu estudo/estudei em uma universidade de música", "Yes, I study/studied at a music university", "Oui, j'étudie/ai étudié dans une université de musique"]
        - 4: ["Outro", "Other", "Autre"]