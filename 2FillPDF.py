import pymupdf

doc = pymupdf.open(r"C:\Users\piard\1 L Capital AG\1LC_ALL - General\1 - Research\Mathias\Temp - to be deleted any time\edited_SubDoc Template-Sejda.pdf")  # Open PDF


# This is just an example on how to create directly the widget or write the text in the pdf from python
#page = doc[0]  # Get the first page

#pt1 =pymupdf.Point(50, 80)  # Define the first point

#page.insert_text(pt1, "Name", fontsize=12, color=(0, 0, 0))  # Insert text at the first point

#wgt = pymupdf.Widget()  # Create a widget object for the text field
#wgt.field_name = "name-text"
#wgt.field_type  =7
#wgt.font_size = 10
#wgt.rect = pymupdf.Rect(140, 65, 300, 85)  # Define the rectangle for the text field
#page.add_widget(wgt)  # Add the widget to the page

#doc.save(r"C:\Users\piard\1 L Capital AG\1LC_ALL - General\1 - Research\Mathias\Temp - to be deleted any time\edited_SubDoc Template-pymupdf.pdf")  # Save the modified PDF

for page in doc:
    for widget in page.widgets():
        print(f"Field Name: {widget.field_name}, Type: {widget.field_type_string}")


for page in doc:
    for widget in page.widgets():
        if widget.field_name == "Amount_in_words_EUR":
            # Get the widget's position
            rect = widget.rect

            # Access the annotation associated with the widget (optional)
            # annot = widget.annot

            # Delete the annotation (optional)
            # page.delete_annot(annot)

            # Add a new text annotation at the same position
            page.insert_text(
                point=rect.bottom_left,  # Position
                text="two million united states dollars",
                fontsize=10,
                fontname="helv",  # Use a standard font
                color=(0, 0, 0)  # Black color
            )


doc.save(r"C:\Users\piard\1 L Capital AG\1LC_ALL - General\1 - Research\Mathias\Temp - to be deleted any time\edited-SubDoc Template-rewriteWidget.pdf")