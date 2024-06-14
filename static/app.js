class Game{
  constructor(id, seconds = 60) {
    this.seconds = seconds;
    this.showTimer();
    
    this.score = 0;
    this.words = new Set();
    this.board = $(`#${id}`);
    this.timer = setInterval(this.tick.bind(this), 1000);
    
    $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
  }
  
  showWord(word) {
    $(".words", this.board).append($("<li>", { text: word }));
  }
  
  showScore() {
    $(".score", this.board).text(this.score);
  }
  
  showMessage(message, cls) {
    $(".message", this.board)
      .text(message)
      .removeClass()
      .addClass(`message ${cls}`);
  }
  
  async handleSubmit(event) {
    event.preventDefault();
    const $word = $(".word", this.board);
    
    let word = $word.val();
    if (!word) return;
    
    if (this.words.has(word)) {
      this.showMessage(`${word} already found`, "err");
      return
    }
    
    const response = await axios.get("/check-guess", { params: { word: word } });
    if (response.data.result === "not-word") {
      this.showMessage(`${word} is not a valid word`, "err");
    } else if (response.data.result === "not-on-board") {
      this.showMessage(`${word} is not on this board`, "err");
    } else {
      this.showWord(word);
      this.score += word.length;
      this.showScore();
      this.words.add(word);
      this.showMessage(`Added "${word}"`, "ok");
    }
    
    $word.val("").focus();
  }
  
  showTimer() {
    $(".timer", this.board).text(this.seconds);
  }
  
  async tick() {
    this.seconds -= 1;
    this.showTimer();
    
    if (this.seconds === 0) {
      clearInterval(this.timer);
      await this.scoreGame();
    }
  }
  
  async scoreGame() {
    $(".add-word", this.board).hide();
    const response = await axios.post("/post-score", { score: this.score });
    if (response.data.brokeRecord) {
      this.showMessage(`New Record! ${this.score}`, "ok");
    } else {
      this.showMessage(`Final Score: ${this.score}`, "ok");
    }
  }
}

let game = new Game("boggle", 60);
