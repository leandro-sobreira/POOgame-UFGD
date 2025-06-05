# POOgame-UFGD


## Marcos - 
A minha parte está sendo desenvolver a interface gráfica, fiz uma tela inicial, uma de seleção de jogos, agora estou implementando uma tela pro BlackJack.  
Meu arquivo principal é o `game_sprites`, que tem basicamente todas as minhas telas. Ele também usa o `config.py` pra acessar alguns dados.

## Classes principais

- O `Main` cria uma classe chamada `Intro` pra iniciar o jogo.  
  Ela inicia o background, sons, desenha toda a tela, usando também objetos de botões controláveis pelas setas.

```python
  tela_intro = intro(screen, "CARD GAME", "Assets/fonts/Ghost Shadow.ttf", 64, 1)
  jogo_selecionado = tela_intro.loop()
  print("Jogo selecionado:", jogo_selecionado)
  del tela_intro  # libera referência para coletor de lixo
  ```

- A `Intro` cria outro objeto pra seleção de jogos que funciona de forma parecida e devolve pra `Intro`.  
  Em geral, o objetivo desses dois é devolver um número que representa o jogo pra `Main`.


```python
  self.jogo = GameSelect(self.screen, self.ok, self.select_sound).loop()
```



- O `Main` então chama a `TelaCartas`, que usa uma classe abstrata pra criar toda a tela.  
  Nela contém botões de adição de cartas e uma tela de resultado.


```python
  if jogo_selecionado == 3:
    Telacartas(screen).loop();
```