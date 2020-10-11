function cost(vboard){
  let score = 0
  for(let pos = 0; pos <= vboard.length; pos++){ //using ...prev_moves below jsut to get the first cpos
    if(vboard[pos] & Tiles.P2){ //for every red drought
      score-=2
      if(vboard[pos] & Tiles.QUEEN){
        score-=1
      }
    }
    if(vboard[pos] & Tiles.P1){
      score+=2
      if(vboard[pos] & Tiles.QUEEN){
        score+=1
      }
    }

  }
  return score;
}

function negamax(is_maximizing){  //the turn booleans are awfull
  let vboard = Array.from(board)
  console.log("negamax")
  print_arr(vboard)
  let color = is_maximizing ? 1 : -1
  let res = negamax_rec(color, MAX_DEPTH, -Infinity, Infinity, vboard)
  console.log(res[0]*color,res[1])
  return res[1] ? res[1] : null
}

function negamax_rec(color, depth, a, b, vboard){ //a,b for alpha beta pruning
  if(depth == 0){
    return color*cost(vboard)
  }

  let mvs = calc_all_moves(color == 1, vboard) //the turn booleans are awfull and misleading
  if(mvs.length == 0){
    return color*103 //brak ruchów to gg
  }

  let best_move = null
  let best_score = -Infinity
  for(let m of mvs){
    //apply the move
    let start = m.mpath[0]
    let end = getLast(m.mpath)
    let moved_type = vboard[start]
    let killed_his = []

    vboard[start] = Tiles.FREE
    vboard[end] = moved_type
    for(let k of m.kpath){
      killed_his.push(vboard[k])
      vboard[k] = Tiles.FREE
    }
    // update_queens(vboard)

    let tmp = -negamax_rec(-color, depth-1, -b, -a, vboard)

    // unupdate_queens(vboard)
    // unapply the move
    console.log(depth, tmp)
    print_arr(vboard)
    vboard[end] = Tiles.FREE
    vboard[start] = moved_type
    for(let i = 0; i < m.kpath.length; i++){
      vboard[m.kpath[i]] = killed_his[i]
    }

    // alpha beta pruning
    if(tmp > best_score){
      best_score = tmp
      best_move = m
    }
    a = Math.max(a, best_score)
    if(a >= b)break; //cut-off!
  }
  
  if(depth == MAX_DEPTH)return [best_score, best_move]
  else return best_score
}

//checks if a position is reachable from a given postition
//dx and dy arefor direction,
//if the enemy is null, acts as a normal move
//if the enemy is set its a killing jump
function can_move(pos, dx, dy, enemy, prev_moves=[], tab){
 // console.log(pos,dx,dy,enemy,prev_moves,tab)
  if(enemy === null){
    if(!(pos%8 == 0 && dx == -1) && !(pos%8 == 7 && dx == 1)){
      let mask = (1<<4)|(1<<6) //AVAIABLE and KILLMOWe
      return tab[pos+dy*8+dx]==0 || tab[pos+dy*8+dx] & mask
    }
  }
  let end = pos+dy*8*2+2*dx;
  //checks if there is enough space horizontally
  if(dx*(pos%8) < dx*(end)%8){
    //checks if there is enough space vertically
    //it wont crash if pos==15 dx = 1, coz the first check forbids that
    if(0<= end && end <= 63){
      if(tab[pos+dy*8+dx] & enemy && tab[end] == Tiles.FREE){
        return !prev_moves.includes(end)//if havent been there before
      }
    }
  } 
}

function calc_all_moves(curr_p1, vboard){
  //console.log(vboard)
  let possible_moves = []
  //i is the tile from which we check the moves
  let curr = curr_p1 ? Tiles.P1 : Tiles.P2
  let enemy = curr_p1 ? Tiles.P2 : Tiles.P1
  let dir = curr_p1 ? -1 : 1

  for(let pos = 0; pos <= 63; pos++){ //using ...prev_moves below jsut to get the first cpos
    if(vboard[pos] & curr){ //for every red drought (may be queen)
      possible_moves.push(...calc_moves_from_pos(enemy, dir, vboard, [pos]))
    }
  }
  return possible_moves;
}

//same as move_path and kill_path but cpos dont want to overuse the variables
function calc_moves_from_pos(enemy, dir, vboard, visited_tiles=[], killed_tiles=[]){
  let res_moves = []
  let pos = getLast(visited_tiles)
  let multikill = killed_tiles.length > 0
  let is_queen = vboard[pos] & Tiles.QUEEN

  if(!multikill){ //cant move normally if has killed already
    for(let dx = -1; dx <= 1; dx+=2){ //normal moves
      for(let dy = -1; dy <= 1; dy+=2){ //reverse moves
        if(dy == -1 && !is_queen)continue;
        if(can_move(pos, dx, dy*dir, null, [], vboard)){
          let end = pos+dy*dir*8+dx;
          res_moves.push(new Move([...visited_tiles, end], []))
        }
      }
    }
  }
  for(let dx = -1; dx <= 1; dx+=2){ //kills
    for(let dy = -1; dy <= 1; dy+=2){
      //responsible for the reverse killing in series
      if(dy == -1 && !multikill && !is_queen)continue;
      if(can_move(pos, dx, dy*dir, enemy, visited_tiles, vboard)){
        let end = pos+(dy*dir*8+dx)*2
        let killed_index = Math.floor((pos+end)/2)
        //add this jump
        res_moves.push(new Move([...visited_tiles, end], [...killed_tiles, killed_index]))
        //recursively find all longer jumps
        res_moves.push(...calc_moves_from_pos(enemy, dir, vboard, [...visited_tiles, end], [...killed_tiles, killed_index]))
      }
    }
  }
  return res_moves;
}

function minIndex(tab){
  let min_val = tab[0]
  let min_index = 0
  for(let i = 1; i < tab.length; i++){
    if(min_val > tab[i]){
      min_val = tab[i]
      min_index = i
    }
  }
  return min_index
}
function maxIndex(tab){
  let max_val = tab[0]
  let max_index = 0
  for(let i = 1; i < tab.length; i++){
    if(max_val < tab[i]){
      max_val = tab[i]
      max_index = i
    }
  }
  return max_index
}

function print_arr(arr){
  for(let j = 0 ; j < 8; j++){
    tmp = []
    for(let i = j*8 ; i < j*8+8; i++){
      tmp.push(Math.abs(arr[i]))
    }
    console.log(tmp)
  }
  console.log("\n")
}