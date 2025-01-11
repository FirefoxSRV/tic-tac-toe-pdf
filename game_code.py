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
  >>
  /Rotate 0
  /Type /Page
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
    this.getField("T_score").value = `X: ${score_x} - O: ${score_o}`;
}

function check_winner() {
    // Check rows
    for (var i = 0; i < 3; i++) {
        if (game_board[i][0] !== '' && 
            game_board[i][0] === game_board[i][1] && 
            game_board[i][1] === game_board[i][2]) {
            return game_board[i][0];
        }
    }
    
    // Check columns
    for (var j = 0; j < 3; j++) {
        if (game_board[0][j] !== '' && 
            game_board[0][j] === game_board[1][j] && 
            game_board[1][j] === game_board[2][j]) {
            return game_board[0][j];
        }
    }
    
    // Check diagonals
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
        this.getField(`B_${row}_${col}`).buttonSetCaption(current_player);
        
        var winner = check_winner();
        if (winner) {
            if (winner === 'X') score_x++;
            else score_o++;
            update_score();
            app.alert(`Player ${winner} wins!`);
            disable_board();
        } else if (check_draw()) {
            app.alert("It's a draw!");
            disable_board();
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
            this.getField(`B_${i}_${j}`).buttonSetCaption('');
        }
    }
    
    enable_board();
    update_turn_indicator();
}

// Initialize the game
update_turn_indicator();
update_score();

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
  /FT /Btn
  /Ff 65536
  /MK <<
    /BG [
      0.9 0.9 0.9
    ]
  >>
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

RESET_BUTTON = """
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
      0.8 0.8 1.0
    ]
    /CA (Reset Game)
  >>
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (B_reset)
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

# Constants for layout
CELL_SIZE = 80
GRID_OFF_X = 200
GRID_OFF_Y = 400

fields_text = ""
field_indexes = []
obj_idx_ctr = 50

def add_field(field):
    global fields_text, field_indexes, obj_idx_ctr
    fields_text += field
    field_indexes.append(obj_idx_ctr)
    obj_idx_ctr += 1

# Add game cells
for row in range(3):
    for col in range(3):
        # Add click handler script
        script = SCRIPT_OBJ
        script = script.replace("###IDX###", f"{obj_idx_ctr} 0")
        script = script.replace("###CONTENT###", f"make_move({row}, {col});")
        add_field(script)
        
        # Add cell button
        cell = CELL_BUTTON
        cell = cell.replace("###IDX###", f"{obj_idx_ctr} 0")
        cell = cell.replace("###SCRIPT_IDX###", f"{obj_idx_ctr-1} 0")
        cell = cell.replace("###ROW###", str(row))
        cell = cell.replace("###COL###", str(col))
        
        x = GRID_OFF_X + (col * CELL_SIZE)
        y = GRID_OFF_Y - (row * CELL_SIZE)
        cell = cell.replace("###RECT###", f"{x} {y} {x + CELL_SIZE} {y + CELL_SIZE}")
        
        add_field(cell)


reset_script = SCRIPT_OBJ
reset_script = reset_script.replace("###IDX###", f"{obj_idx_ctr} 0")
reset_script = reset_script.replace("###CONTENT###", "reset_game();")
add_field(reset_script)


reset_button = RESET_BUTTON
reset_button = reset_button.replace("###IDX###", f"{obj_idx_ctr} 0")
reset_button = reset_button.replace("###SCRIPT_IDX###", f"{obj_idx_ctr-1} 0")
reset_button = reset_button.replace("###RECT###", f"{GRID_OFF_X} {GRID_OFF_Y + 50} {GRID_OFF_X + 240} {GRID_OFF_Y + 80}")
add_field(reset_button)

turn_text = TEXT_FIELD
turn_text = turn_text.replace("###IDX###", f"{obj_idx_ctr} 0")
turn_text = turn_text.replace("###NAME###", "T_turn")
turn_text = turn_text.replace("###VALUE###", "Current Turn: X")
turn_text = turn_text.replace("###RECT###", f"{GRID_OFF_X} {GRID_OFF_Y + 100} {GRID_OFF_X + 240} {GRID_OFF_Y + 130}")
add_field(turn_text)


score_text = TEXT_FIELD
score_text = score_text.replace("###IDX###", f"{obj_idx_ctr} 0")
score_text = score_text.replace("###NAME###", "T_score")
score_text = score_text.replace("###VALUE###", "X: 0 - O: 0")
score_text = score_text.replace("###RECT###", f"{GRID_OFF_X} {GRID_OFF_Y + 140} {GRID_OFF_X + 240} {GRID_OFF_Y + 170}")
add_field(score_text)


filled_pdf = PDF_FILE_TEMPLATE.replace("###FIELDS###", fields_text)
filled_pdf = filled_pdf.replace("###FIELD_LIST###", " ".join([f"{i} 0 R" for i in field_indexes]))

with open("tictactoe.pdf", "w") as pdffile:
    pdffile.write(filled_pdf)