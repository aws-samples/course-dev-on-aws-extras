import React, { useState } from 'react';
import { Row, Col, Card, Button, Container, Form, ListGroup, Badge, Spinner, Jumbotron} from 'react-bootstrap';
import { CountdownCircleTimer } from 'react-countdown-circle-timer'
import { WebsocketEndpoint } from './config'

var TRIVIA_STEP = {
  STEP_GETSTARTED : {value: 0},
  STEP_JOINGAME: {value: 1},
  STEP_WAITING : {value: 2},
  STEP_QUESTIONS : {value: 3},
  STEP_GAMEOVER : {value: 4},
};

function GetStarted(props) {
  if (props.currentStep !== TRIVIA_STEP.STEP_GETSTARTED) {
    return null
  }

  return (<Card>
    <Card.Body>
      <Card.Title>Get Started</Card.Title>
      <Card.Text>
        Click the button below to start a new game.
      </Card.Text>
      <Button variant="primary" onClick={props.onNewGame}>Create a New Game</Button>
    </Card.Body>
  </Card>);
}

function JoinGame(props) {
  if (props.currentStep !== TRIVIA_STEP.STEP_JOINGAME) {
    return null
  }
  return (
    <Card>
      <Card.Body>
        <Card.Title>Join Game</Card.Title>
        <Card.Text>
          You've been invited to join a game!
        </Card.Text>
        <Button variant="primary" onClick={props.onJoinGame}>Join</Button>
      </Card.Body>
    </Card>
  );
}

function Waiting(props) {
  if (props.currentStep !== TRIVIA_STEP.STEP_WAITING) {
    return null
  }
  const invitelink = new URL(`#newgame/${props.gameId}`, document.baseURI).href;
  const inviteBody = (props.gameId) ? (
    <Card.Text>
      Share the link below with players joining the game
      <Form.Control type="text" value={invitelink} readOnly />
      <Button variant="primary" onClick={props.onStartGame}>Start Game</Button>
    </Card.Text>
    ) : (
      <Spinner animation="grow" variant="secondary" />
  );

  return (
    <Card>
      <Card.Body>
        <Card.Title>Waiting for players</Card.Title>
        {inviteBody}
      </Card.Body>
    </Card>
  );
}

function Questions(props) {
  const [activeButton, setActiveButton] = useState(null);

  const answerClick = (key, id, option) => {
    props.onAnswer(id, option);
    setActiveButton(key);
  }

  if (props.currentStep !== TRIVIA_STEP.STEP_QUESTIONS) {
    return null
  }

  var questionBody = !props.question ? (
    <Spinner animation="grow" variant="secondary" />
  ) : (
    <Col lg="8">
      <b>{props.question.question}</b>
      <div className="d-grid gap-2">
      {props.question.options.map((option, i) => {
        const myKey = props.question.id + "-" + i;
        return (
          <Button
           key={myKey}
           variant={activeButton===myKey ? "success" : "secondary"}
           onClick={() => answerClick(myKey, props.question.id, option)}
           size="lg" block>
            {option}
          </Button>
        )
      })}
      </div>
    </Col>
  );

  return (
    <Card>
      <Card.Body>
        <Card.Title>Let's Play!</Card.Title>
          {questionBody}
      </Card.Body>
    </Card>
  );
}

function Players(props) {
  if (!props.playerList) {
    return null;
  }
  return (
    <Card>
      <Card.Body>
        <Card.Title>Players</Card.Title>

        <ListGroup>
        {props.playerList && props.playerList.filter((player)=>player.currentPlayer).map((player, i) => {
            return (<ListGroup.Item key={player.connectionId} variant="primary" className="d-flex justify-content-between align-items-center">
              <span style={{color:player.playerName}}>&#11044; <span className="small" style={{color:"Black"}}>{player.playerName}</span></span>
              <Badge pill variant="dark">{player.score}</Badge>
            </ListGroup.Item>)
         })}
         </ListGroup>
         <p></p>
         <ListGroup>
        {props.playerList ? props.playerList.filter((player)=>!player.currentPlayer).map((player, i) => {
            return (<ListGroup.Item key={player.connectionId} className="d-flex justify-content-between align-items-center">
              <span style={{color:player.playerName}}>&#11044; <span className="small" style={{color:"Black"}}>{player.playerName}</span></span>
              <Badge pill variant="dark">{player.score}</Badge>
            </ListGroup.Item>)
         }) : <div>no players</div>}

        </ListGroup>
      </Card.Body>
    </Card>
  );
}

function GameOver(props) {
  if (props.currentStep !== TRIVIA_STEP.STEP_GAMEOVER) {
    return null
  }
  const restart = () => {
    document.location = document.baseURI;
  };

  return (
    <Jumbotron>
    <h1>Game Completed!</h1>
    <p>
    </p>
    <p>
      <Button variant="primary" onClick={()=>restart()}>Restart</Button>
    </p>
  </Jumbotron>
  );
}

class App extends React.Component {
  ws = new WebSocket(WebsocketEndpoint);

  constructor(props) {
    super(props);
    this.state = {
      currentStep: document.location.hash.startsWith('#newgame') ? TRIVIA_STEP.STEP_JOINGAME : TRIVIA_STEP.STEP_GETSTARTED,
      connected: false,
      playerList: null,
      gameId: document.location.hash.startsWith('#newgame') ? document.location.hash.replace('#newgame/', '') :  null,
      question: null
    };
  }

  newGame() {
    var message = JSON.stringify({"action":"newgame"});
    this.ws.send(message);
    this.setState({currentStep: TRIVIA_STEP.STEP_WAITING});
  }

  joinGame() {
    var message = JSON.stringify({"action":"joingame", "gameid": this.state.gameId});
    this.ws.send(message);
    this.setState({currentStep: TRIVIA_STEP.STEP_QUESTIONS});
  }

  startGame() {
    var message = JSON.stringify({"action":"startgame", "gameid": this.state.gameId});
    this.ws.send(message);
    this.setState({currentStep: TRIVIA_STEP.STEP_QUESTIONS});
  }

  answer(questionId, answer) {
    var message = JSON.stringify({
      "action":"answer",
      "gameid": this.state.gameId,
      "questionid": questionId,
      "answer": answer
    });
    this.ws.send(message);
  }

  componentDidMount() {
      this.ws.onopen = () => {
        this.setState({connected: true});
      }

      this.ws.onmessage = evt => {
        const message = JSON.parse(evt.data)

        switch(message.action) {
          case "gamecreated":
            this.setState({gameId: message.gameId});
            break;
          case "playerlist":
            this.setState({playerList: message.players.splice(0)});
            break;
          case "question":
            this.setState({question: message.question})
            break;
          case "gameover":
            this.setState({currentStep: TRIVIA_STEP.STEP_GAMEOVER});
            break;
          default:
            break;
        }
      }

      this.ws.onclose = () => {
        this.setState({connected: false});
      }

  }


  render() {
    return (
      <Container className="p-3">
      <Row>
      <Col>
        <GetStarted currentStep={this.state.currentStep} onNewGame={() => this.newGame()} />
        <JoinGame currentStep={this.state.currentStep} onJoinGame={() => this.joinGame()} gameId={this.state.gameId} />
        <Waiting currentStep={this.state.currentStep} onStartGame={() => this.startGame()} gameId={this.state.gameId} />
        <Questions currentStep={this.state.currentStep} onAnswer={(questionId, answer) => this.answer(questionId, answer)} question={this.state.question}  />
        <GameOver currentStep={this.state.currentStep} />
        {this.state.connected ? <small>&#129001; connected</small> :  <small>&#128997; disconnected</small>}
      </Col>
      <Col xs={3}>
        <Players playerList={this.state.playerList}/>
        <br/>
        <div className="d-flex justify-content-center">
        {this.state.question && <CountdownCircleTimer
          key={this.state.question.id}
          size={120}
          isPlaying
          duration={5}
          colors={[["#007bff"]]}
        >
          {({ remainingTime }) => remainingTime}
        </CountdownCircleTimer>}
        </div>
      </Col>

      </Row>
      </Container>
    );
  }
}

export default App;
