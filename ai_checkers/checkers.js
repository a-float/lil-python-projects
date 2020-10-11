const c_size = 60;
let is_turn_P1 = true; 
const ANIM_TIME = 10;
const KTM = 1.5; //KILL TIME MULTIPLIER
let MAX_DEPTH = 2;
let IS_P2_BOT = true;
let IS_P1_BOT = true;
let ENABLE_PRUNNING = true

//creating an enum
const Tiles = {
   FREE: 0,
   P1: 1,
   P2: 2,
   QUEEN: 4,
   AVAILABLE: 16,
   SELECTED: 32,
   KILLMOVE: 64,
};

Object.freeze(Tiles);

let Colors;

class Move{ //for the ai
  constructor(mpath=[], kpath=[]){
    this.mpath = mpath
    this.kpath = kpath
  }
  clear(m = [], k = []){
    this.mpath = m
    this.kpath = k
  }
}

let board;

let selected = -1;
let is_killing = false; //did the player choose a place to move which involves killing
let can_kill = false; //is there a possibility of killing
let move_time_left = 0;

let player_move = new Move() //player fill it up
let anim_mpath = []
let end_anim_pos;
let moving_piece_type;
let game_over = false

let domTURN = document.getElementById("turn");
let checkBoxP1 = document.getElementById("myCheckP1");
let checkBoxP2 = document.getElementById("myCheckP2");
let textP1 = document.getElementById("textP1");
let textP2 = document.getElementById("textP2");

function setup() {
  createCanvas(480, 480);

  Colors = {
    DARK_BOARD: color(40,40,80),
    P1: color(255),
    P2: color(200,40,40),
    SELECTED: color(190,190,40),
    AVAILABLE: color(230,230,40)
  };
  Object.freeze(Colors);

  frameRate(60);
  stroke(0);
  strokeWeight(1);

  selected = -1;
  is_killing = false; //did the player choose a place to move which involves killing
  move_time_left = 0;

  player_move = new Move() //player fill it up
  anim_mpath = []
  game_over = false
  is_turn_P1 = true

  board = new Array(64).fill(Tiles.FREE);
  setup_draughts()
  draw_board();
  updateDOM();
}

function draw(){
    draw_board();
    updateDOM();
    strokeWeight(3)
    stroke(60)

    if(game_over)noLoop()
    if(move_time_left > 0){ //animating moves
      let x,y
      if(Math.abs(anim_mpath[0].x - anim_mpath[1].x) > 1*c_size){ //only killing moves
        let move_step = anim_mpath.length - 1 - Math.ceil(move_time_left/(ANIM_TIME*KTM));
        let lerp_val = (KTM*ANIM_TIME - (move_time_left-1)%(KTM*ANIM_TIME))/(KTM*ANIM_TIME)
        x = lerp(anim_mpath[move_step].x, anim_mpath[move_step+1].x, lerp_val);
        y = lerp(anim_mpath[move_step].y, anim_mpath[move_step+1].y, lerp_val);
      } 
      else{ //just moving
        let lerp_val = (ANIM_TIME - move_time_left+1)/(ANIM_TIME)
        x = lerp(anim_mpath[0].x, anim_mpath[1].x, lerp_val);
        y = lerp(anim_mpath[0].y, anim_mpath[1].y, lerp_val);
      }

      if(!is_turn_P1)fill(Colors.P1);
      else fill(Colors.P2);
      ellipse(x+0.5*c_size, y +0.5*c_size, c_size*.6, c_size*.6);
      if(moving_piece_type & Tiles.QUEEN){
        fill(60)
        ellipse(x+0.5*c_size, y +0.5*c_size, c_size*.2, c_size*.2);
      }

      move_time_left -= 1;

      if(move_time_left <= 0){ //end animating
        board[end_anim_pos] = moving_piece_type;
        anim_mpath = []
        update_queens(board);
        let mvs = calc_all_moves(is_turn_P1, board)
        if(mvs.length == 0){
          endGame(!is_turn_P1) //has to be negated
        }
      }
    }
    else if((is_turn_P1 && IS_P1_BOT) || (!is_turn_P1 && IS_P2_BOT)){
      bot_move = negamax(is_turn_P1)
      if(bot_move == null){
        endGame(is_turn_P1)
        return
      }
      //console.log(bot_move)
      exec_move(bot_move)
    }
}

function draw_board(){
  background(255);
  fill(255)
  rect(0,0,width,height)
  fill(Colors.DARK_BOARD);
  //create the checkerboard
  for(let i = 0; i < 8; i++){
    for(let j = i%2; j < 8; j+=2){
      rect(i*c_size, j*c_size, c_size, c_size)
    }
  }
  strokeWeight(3)
  stroke(60)
  for(let i = 0; i < board.length; i++){    //could turn the 3 ifs below into one
    if(board[i] & (Tiles.AVAILABLE | Tiles.KILLMOVE)){
      fill(Colors.AVAILABLE);
      rect((i%8)*c_size, (Math.floor(i/8))*c_size, c_size, c_size)
    }
    if(board[i] & Tiles.KILLMOVE){
      fill(200,50,50);
      rect((i%8)*c_size, (Math.floor(i/8))*c_size, c_size, c_size)
    }
    if(board[i] & Tiles.SELECTED){
      fill(Colors.SELECTED);
      rect((i%8)*c_size, (Math.floor(i/8))*c_size, c_size, c_size)
    }
    if(board[i] & Tiles.P1){
      fill(Colors.P1); 
      ellipse((i%8 + .5)*c_size, (Math.floor(i/8)+.5)*c_size, c_size*.6, c_size*.6)
    }
    else if(board[i] & Tiles.P2){
      fill(Colors.P2)
      ellipse((i%8 + .5)*c_size, (Math.floor(i/8)+.5)*c_size, c_size*.6, c_size*.6)
    }
    if(board[i] & Tiles.QUEEN){
      fill(60)
      ellipse((i%8 + .5)*c_size, (Math.floor(i/8)+.5)*c_size, c_size*.2, c_size*.2)
    }
  }
  show_numbers();
}

function setup_draughts(){
  for(let i = 0; i < 64; i++){
    if((Math.floor(i/8)+i%2)%2){
      if(i<=23)board[i] = Tiles.P2;
      else if(i >= 40)board[i] = Tiles.P1;
    }
  }
}

function update_available(){
  let mask = Tiles.AVAILABLE | Tiles.KILLMOVE
  for(let i = 0; i < 64; i++){
    if(board[i] & mask){
      board[i] &= ~mask;
    }
  }
  //i is the tile from which we check the moves
  i = getLast(player_move.mpath) //should never be an empty array
  let enemy = is_turn_P1 ? Tiles.P2 : Tiles.P1
  let dir = is_turn_P1 ? -1 : 1
  let is_queen = board[i] & Tiles.QUEEN

  let mvs = calc_moves_from_pos(enemy, dir, board, player_move.mpath, player_move.kpath)
  for(let m of mvs){
    if(m.kpath.length > 0){
      can_kill = true
      board[getLast(m.mpath)] |= Tiles.KILLMOVE
    }
    else{
      board[getLast(m.mpath)] |= Tiles.AVAILABLE
    }
  }
}

function mousePressed(){
  // if(!is_turn_P1)return;
  player_tile = is_turn_P1 ? Tiles.P1 : Tiles.P2;
  if(mouseX > 0 && mouseX < width && mouseY > 0 && mouseY < height){
    pos = Math.floor(mouseY/c_size)*8 + Math.floor(mouseX/c_size);
    //console.log("click at " + pos);
    if(pos == selected){ //unselecting
      selected = -1;
      board[pos] &= ~Tiles.SELECTED
      player_move.clear()
      is_killing = false;
    }
    else if(is_killing && pos == getLast(player_move.mpath)){  //break the killing spree
      exec_move(move_path, kill_path)
    }
    else if(board[pos] & player_tile){ //selecting a draught (or switching selected)
      if(selected != -1)board[selected] &= ~Tiles.SELECTED
        ;
      selected = pos
      board[pos] |= Tiles.SELECTED
      player_move.clear([pos])
      is_killing = false;
    }
    else if(selected != -1 && board[pos] & Tiles.AVAILABLE){ //moving
      player_move.mpath.push(pos)
      exec_move(player_move)
    }
    else if(selected != -1 && board[pos] & Tiles.KILLMOVE){ //killing
      is_killing = true;
      player_move.kpath.push(Math.floor((pos+getLast(player_move.mpath))/2));
      player_move.mpath.push(pos);
      board[pos] |= Tiles.AVAILABLE; //as a mark and used to break killing spree
    }
    can_kill = false;
    update_available();
    if(is_killing && !can_kill){
      exec_move(player_move); //make the kills
    }
  }
}

function exec_move(move){
  //setting up moving animation
  let mpath = move.mpath
  let kpath = move.kpath
  move_time_left = ANIM_TIME*((mpath.length-1)+((kpath.length)*(KTM-1)))
  
  points = []
  for(let p of mpath){
    v = createVector(p%8*c_size,Math.floor(p/8)*c_size)
    points.push(v)
  }
  if(kpath != []){
    for(let k of kpath){
      board[k] = Tiles.FREE
    }
    is_killing = false;
  }
  anim_mpath = points;
  selected = -1;
  end_anim_pos = getLast(mpath)
  moving_piece_type = board[mpath[0]] & (Tiles.QUEEN | Tiles.P1 | Tiles.P2)
  board[mpath[0]] = Tiles.FREE;
  move.clear() //clears player or bot
  is_turn_P1 = !is_turn_P1
  updateDOM()
  update_available()
}

function updateDOM(){
  domTURN.innerHTML = is_turn_P1 ? "white" : "red";
  domTURN.style.color = is_turn_P1 ? Colors.P1 : Colors.P2;
  IS_P1_BOT = checkBoxP1.checked
  IS_P2_BOT = checkBoxP2.checked
  if(IS_P1_BOT){
    textP1.style.display = "block";
  } else {
    textP1.style.display = "none";
  }
  if(IS_P2_BOT){
    textP2.style.display = "block";
  } else {
    textP2.style.display = "none";
  }

}

function show_numbers(){
  fill(255)
  for(let i = 0; i < 64; i++){
    text(i, (i%8)*c_size+3, (Math.floor(i/8))*c_size+3, c_size, c_size)
  }
}

function getLast(tab){
  return tab[tab.length-1]
}

function endGame( who_won){
  game_over = true
  console.log(str(who_won ? "white" : "red") + " has won!")
}

function update_queens(board){
  //make QUEENS
  for(let i = 64-8; i < 64; i++){
    if(board[i] & Tiles.P2 & ~Tiles.QUEEN)board[i] |= Tiles.QUEEN;
  }
  for(let i = 0; i < 8; i++){
    if(board[i] & Tiles.P1 & ~Tiles.QUEEN)board[i] |= Tiles.QUEEN;
  }
}