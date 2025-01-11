PDF_FILE_TEMPLATE = """
%PDF-1.6

% Root
1 0 obj
<<
  /AcroForm <<
    /Fields [ ###FIELD_LIST### ]
  >>
  /Pages 2 0 R
  /OpenAction 17 0 R
  /Type /Catalog
>>
endobj

2 0 obj
<<
  /Count 1
  /Kids [
    16 0 R
  ]
  /Type /Pages
>>

%% Annots Page 1 (also used as overall fields list)
21 0 obj
[
  ###FIELD_LIST###
]
endobj

###FIELDS###

%% Page 1
16 0 obj
<<
  /Annots 21 0 R
  /Contents 3 0 R
  /CropBox [
    0.0
    0.0
    612.0
    792.0
  ]
  /MediaBox [
    0.0
    0.0
    612.0
    792.0
  ]
  /Parent 2 0 R
  /Resources <<
    /Font <<
      /F1 22 0 R
    >>
  >>
  /Rotate 0
  /Type /Page
>>
endobj

22 0 obj
<<
  /BaseFont /Helvetica
  /Encoding /WinAnsiEncoding
  /Name /F1
  /Subtype /Type1
  /Type /Font
>>
endobj

3 0 obj
<< >>
stream
endstream
endobj

17 0 obj
<<
  /JS 42 0 R
  /S /JavaScript
>>
endobj

42 0 obj
<< >>
stream

var current_player = 'X';
var score_x = 0;
var score_o = 0;
var game_board = [
    ['', '', ''],
    ['', '', ''],
    ['', '', '']
];

function update_turn_indicator() {
    this.getField("T_turn").value = `Current Turn: ${current_player}`;
}

function update_score() {
    this.getField("T_score").value = `Score - X: ${score_x} | O: ${score_o}`;
}

function check_winner() {
    for (var i = 0; i < 3; i++) {
        if (game_board[i][0] !== '' && 
            game_board[i][0] === game_board[i][1] && 
            game_board[i][1] === game_board[i][2]) {
            return game_board[i][0];
        }
    }
    
    for (var j = 0; j < 3; j++) {
        if (game_board[0][j] !== '' && 
            game_board[0][j] === game_board[1][j] && 
            game_board[1][j] === game_board[2][j]) {
            return game_board[0][j];
        }
    }
    
    if (game_board[0][0] !== '' && 
        game_board[0][0] === game_board[1][1] && 
        game_board[1][1] === game_board[2][2]) {
        return game_board[0][0];
    }
    
    if (game_board[0][2] !== '' && 
        game_board[0][2] === game_board[1][1] && 
        game_board[1][1] === game_board[2][0]) {
        return game_board[0][2];
    }
    
    return null;
}

function check_draw() {
    for (var i = 0; i < 3; i++) {
        for (var j = 0; j < 3; j++) {
            if (game_board[i][j] === '') {
                return false;
            }
        }
    }
    return true;
}

function make_move(row, col) {
    if (game_board[row][col] === '') {
        game_board[row][col] = current_player;
        this.getField(`B_${row}_${col}`).value = current_player;
        
        var winner = check_winner();
        if (winner) {
            if (winner === 'X') score_x++;
            else score_o++;
            update_score();
            reset_game();
            app.alert({
                cMsg: `Player ${winner} wins!`,
                cTitle: "Game Over",
                nIcon: 3,
                nType: 0,
                oDoc: this,
                cExec: "start_game();"
            });
        } else if (check_draw()) {
            reset_game();
            app.alert({
                cMsg: "It's a draw!",
                cTitle: "Game Over",
                nIcon: 3,
                nType: 0,
                oDoc: this,
                cExec: "start_game();"
            });
        } else {
            current_player = current_player === 'X' ? 'O' : 'X';
            update_turn_indicator();
        }
    }
}

function disable_board() {
    for (var i = 0; i < 3; i++) {
        for (var j = 0; j < 3; j++) {
            this.getField(`B_${i}_${j}`).readonly = true;
        }
    }
}

function enable_board() {
    for (var i = 0; i < 3; i++) {
        for (var j = 0; j < 3; j++) {
            this.getField(`B_${i}_${j}`).readonly = false;
        }
    }
}

function reset_game() {
    current_player = 'X';
    game_board = [
        ['', '', ''],
        ['', '', ''],
        ['', '', '']
    ];
    
    for (var i = 0; i < 3; i++) {
        for (var j = 0; j < 3; j++) {
            this.getField(`B_${i}_${j}`).value = '';
        }
    }
    
    enable_board();
    update_turn_indicator();
    this.getField("B_start").display = 0; 
    this.getField("B_reset_scores").display = 1;  
}

function start_game() {
    reset_game();
}

function reset_scores() {
    this.submitForm();
}

// Initialize the game
update_turn_indicator();
update_score();
// Initially disable the board
enable_board();
this.getField("B_reset_scores").display = 1;  // Initially show Reset Scores button
this.getField("B_start").display = 0;  // Hide Start button

endstream
endobj

trailer
<<
  /Root 1 0 R
>>

%%EOF
"""

CELL_BUTTON = """
###IDX### obj
<<
  /A <<
    /JS ###SCRIPT_IDX### R
    /S /JavaScript
  >>
  /F 4
  /FT /Tx
  /Ff 1
  /MK <<
    /BG [
      0.9 0.9 0.9
    ]
  >>
  /DA (/F1 40 Tf 0 0 0 rg)
  /Q 1
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (B_###ROW###_###COL###)
  /Type /Annot
>>
endobj
"""

START_BUTTON = """
###IDX### obj
<<
  /A <<
    /JS ###SCRIPT_IDX### R
    /S /JavaScript
  >>
  /F 4
  /FT /Btn
  /Ff 65536
  /MK <<
    /BG [
      0.8 1.0 0.8
    ]
    /CA (Reset Game)
  >>
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (B_start)
  /Type /Annot
>>
endobj
"""

RESET_SCORES_BUTTON = """
###IDX### obj
<<
  /A <<
    /JS ###SCRIPT_IDX### R
    /S /JavaScript
  >>
  /F 4
  /FT /Btn
  /Ff 65536
  /MK <<
    /BG [
      1.0 0.8 0.8
    ]
    /CA (Reset Scores)
  >>
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (B_reset_scores)
  /Type /Annot
>>
endobj
"""

TEXT_FIELD = """
###IDX### obj
<<
  /F 4
  /FT /Tx
  /Ff 1
  /MK <<
  >>
  /DA (/F1 12 Tf 0 0 0 rg)
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (###NAME###)
  /V (###VALUE###)
  /Type /Annot
>>
endobj
"""

SCRIPT_OBJ = """
###IDX### obj
<< >>
stream
###CONTENT###
endstream
endobj
"""

CELL_SIZE = 80
GRID_OFF_X = 200
GRID_OFF_Y = 500

fields_text = ""
field_indexes = []
obj_idx_ctr = 50

def add_field(field):
    global fields_text, field_indexes, obj_idx_ctr
    fields_text += field
    field_indexes.append(obj_idx_ctr)
    obj_idx_ctr += 1

for row in range(3):
    for col in range(3):
        script = SCRIPT_OBJ
        script = script.replace("###IDX###", f"{obj_idx_ctr} 0")
        script = script.replace("###CONTENT###", f"make_move({row}, {col});")
        add_field(script)
        
        cell = CELL_BUTTON
        cell = cell.replace("###IDX###", f"{obj_idx_ctr} 0")
        cell = cell.replace("###SCRIPT_IDX###", f"{obj_idx_ctr-1} 0")
        cell = cell.replace("###ROW###", str(row))
        cell = cell.replace("###COL###", str(col))
        
        x = GRID_OFF_X + (col * CELL_SIZE)
        y = GRID_OFF_Y - (row * CELL_SIZE)
        cell = cell.replace("###RECT###", f"{x} {y} {x + CELL_SIZE} {y + CELL_SIZE}")
        
        add_field(cell)
turn_text_box = """
###IDX### obj
<<
  /F 4
  /FT /Tx
  /Ff 1
  /MK <<
    /BG [ 0.8 0.8 0.8 ]  % Light grey background for box
    /BC [ 0.0 0.0 0.0 ]  % Black border for box
    /S /S
  >>
  /DA (/F1 16 Tf 0 0 0 rg)
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (T_turn)
  /V (Current Turn: X)
  /Type /Annot
>>
endobj
"""
turn_text_box = turn_text_box.replace("###IDX###", f"{obj_idx_ctr} 0")
turn_text_box = turn_text_box.replace("###RECT###", f"{GRID_OFF_X} {GRID_OFF_Y + 160} {GRID_OFF_X + 240} {GRID_OFF_Y + 190}")
add_field(turn_text_box)

score_text_box = """
###IDX### obj
<<
  /F 4
  /FT /Tx
  /Ff 1
  /MK <<
    /BG [ 0.8 0.8 0.8 ]  % Light grey background for box
    /BC [ 0.0 0.0 0.0 ]  % Black border for box
    /S /S
  >>
  /DA (/F1 16 Tf 0 0 0 rg)
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (T_score)
  /V (Score - X: 0 | O: 0)
  /Type /Annot
>>
endobj
"""
score_text_box = score_text_box.replace("###IDX###", f"{obj_idx_ctr} 0")
score_text_box = score_text_box.replace("###RECT###", f"{GRID_OFF_X} {GRID_OFF_Y + 120} {GRID_OFF_X + 240} {GRID_OFF_Y + 150}")
add_field(score_text_box)

start_script = SCRIPT_OBJ
start_script = start_script.replace("###IDX###", f"{obj_idx_ctr} 0")
start_script = start_script.replace("###CONTENT###", "start_game();")
add_field(start_script)

start_button = START_BUTTON
start_button = start_button.replace("###IDX###", f"{obj_idx_ctr} 0")
start_button = start_button.replace("###SCRIPT_IDX###", f"{obj_idx_ctr-1} 0")
start_button = start_button.replace("###RECT###", f"{GRID_OFF_X} {GRID_OFF_Y - 320} {GRID_OFF_X + 240} {GRID_OFF_Y - 290}")
add_field(start_button)

reset_scores_script = SCRIPT_OBJ
reset_scores_script = reset_scores_script.replace("###IDX###", f"{obj_idx_ctr} 0")
reset_scores_script = reset_scores_script.replace("###CONTENT###", "reset_scores();")
add_field(reset_scores_script)

reset_scores_button = RESET_SCORES_BUTTON
reset_scores_button = reset_scores_button.replace("###IDX###", f"{obj_idx_ctr} 0")
reset_scores_button = reset_scores_button.replace("###SCRIPT_IDX###", f"{obj_idx_ctr-1} 0")
reset_scores_button = reset_scores_button.replace("###RECT###", f"{GRID_OFF_X} {GRID_OFF_Y - 290} {GRID_OFF_X + 240} {GRID_OFF_Y - 260}")
add_field(reset_scores_button)


filled_pdf = PDF_FILE_TEMPLATE.replace("###FIELDS###", fields_text)
filled_pdf = filled_pdf.replace("###FIELD_LIST###", " ".join([f"{i} 0 R" for i in field_indexes]))

with open("tictactoe.pdf", "w") as pdffile:
    pdffile.write(filled_pdf)



