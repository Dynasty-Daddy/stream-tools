from constants import SEASON_STATS_BY_POSITION

def generate_stats_html(player_stats_list, fields=SEASON_STATS_BY_POSITION, position="WR", team_color="#1a32e0"):
    """
    Generates an HTML string representing a player stats table with multiple rows.
    Each entry in player_stats_list is one row.
    """
    text_color_css = "#2C3E50"
    header_text_color_css = "#FFFFFF"
    font_family = "'Arial', sans-serif"
    font_size = "18px"
    font_weight = "bold"

    keys_and_labels = fields.get(position, fields["WR"])
    headers = [label for label, _ in keys_and_labels]
    keys = [key for _, key in keys_and_labels]

    col_min_width_px = 80
    row_height_px = 30
    cell_padding_horizontal_px = 15
    cell_padding_vertical_px = 5
    bottom_buffer_px = 5

    header_cells_html = "".join(
        f'<div class="stat-cell header">{header}</div>' for header in headers
    )

    # Generate multiple data rows
    data_rows_html = ""
    for player_stats in player_stats_list:
        row_cells = ""
        for key in keys:
            value = player_stats.get(key, 0)
            
            # Format number nicely
            if isinstance(value, float) and value.is_integer():
                display_value = f"{int(value):,}"
            elif isinstance(value, int):
                display_value = f"{value:,}"
            else:
                display_value = str(value)
            
            row_cells += f'<div class="stat-cell value">{display_value}</div>'
        data_rows_html += f'<div class="data-row">{row_cells}</div>\n'



    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Player Stats Table</title>
        <meta http-equiv="refresh" content="5">
        <style>
            body {{
                margin: 0;
                padding: 0;
                background-color: transparent !important;
                overflow: hidden;
                display: flex;
                justify-content: center;
                align-items: flex-start;
                min-height: 1px;
            }}

            .stats-container {{
                display: flex;
                flex-direction: column;
                width: auto;
                background-color: #FFFFFF;
                border-radius: 4px;
                overflow: hidden;
                padding-bottom: {bottom_buffer_px}px;
            }}

            .header-row, .data-row {{
                display: flex;
                text-align: center;
                min-height: {row_height_px}px;
                align-items: center;
                white-space: nowrap;
            }}

            .header-row {{
                background-color: {team_color};
                color: {header_text_color_css};
            }}

            .stat-cell {{
                flex: 1;
                min-width: {col_min_width_px}px;
                padding: {cell_padding_vertical_px}px {cell_padding_horizontal_px}px;
                font-family: {font_family};
                font-size: {font_size};
                font-weight: {font_weight};
                display: flex;
                justify-content: center;
                align-items: center;
            }}

            .stat-cell.value {{
                color: {text_color_css};
            }}
        </style>
    </head>
    <body>
        <div class="stats-container">
            <div class="header-row">
                {header_cells_html}
            </div>
            {data_rows_html}
        </div>
    </body>
    </html>
    """
    return html_content
