class BoggleGame {
    constructor(){
        this.time = 20;
        this.score = 0;
        this.words = new Set();
        this.timer = setInterval(this.countDown.bind(this), 1000);

        $('.add-word').on('submit',this.checkWord.bind(this));
    }

    countDown(){
        this.time -= 1;
        if(this.time === 0){
            $('.add-word').hide();
            clearInterval(this.timer);
            this.endGame(this.score);
        }
        $('.timer').text(this.time);  
    }

    createMsg(msg){
        $('.msg')
        .text(msg)
        .show()
    }

    async checkWord(e){
        e.preventDefault();
       let guess = $('.word').val()
       if(!guess) return;

       if(this.words.has(guess)){
        $('.msg').text(`Already found ${guess}`);
        return;
       }

       const res = await axios.get('/check-word', {params:{ word: guess }})
       if (res.data.result === 'not-word'){
        this.createMsg(`${guess} is an invalid word.`)
       } else if (res.data.result === 'not-on-board'){
        this.createMsg(`${guess} is not on the board`)
       }else{
        this.score += guess.length;
        this.words.add(guess);
        this.createMsg(`${guess} is a valid word! Great Work!`)
       }
       $('.word').val('')
       $('.word').focus();
    }
    async endGame(){
        $(".add-word").hide();
        const res = await axios.post("/final-score",{score: this.score});
        if(res.data.newRecord){
           this.createMsg(`New Record: ${this.score}`);
        }
        else {
           this.createMsg(`Final Score: ${this.score}`);
        }

    }
}