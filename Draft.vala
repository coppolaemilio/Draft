using Gtk;

public class Draft : Window {

    private TextView text_view;
    
    private string f_name;

    public TextFileViewer () {
        this.title = "Draft";
        this.window_position = WindowPosition.CENTER;
        set_default_size (400, 300);
        
        try {
            this.icon = IconTheme.get_default ().load_icon ("accessories-text-editor", 32, 0);
            } catch (Error e) {
            stderr.printf ("Could not load application icon: %s\n", e.message);
            }


        var toolbar = new Toolbar ();
        toolbar.get_style_context ().add_class (STYLE_CLASS_PRIMARY_TOOLBAR);
        
        var new_button = new ToolButton.from_stock (Stock.NEW);
        new_button.clicked.connect (on_new_clicked);
        
        var open_button = new ToolButton.from_stock (Stock.OPEN);
        open_button.clicked.connect (on_open_clicked);
        
        var menu_button = new ToolButton.from_stock (Stock.PROPERTIES);
        
        var separator = new Gtk.SeparatorToolItem();
        separator.set_draw (false);
        var separator2 = new Gtk.SeparatorToolItem();
        separator2.set_draw (false);
        separator2.set_expand (true);
        
        var save_button = new ToolButton.from_stock (Stock.SAVE);
        save_button.clicked.connect (on_save_clicked);
        
        var save_as_button = new ToolButton.from_stock (Stock.SAVE_AS);
        save_as_button.clicked.connect (on_save_as_clicked);
        
        var bold_button = new ToolButton.from_stock (Stock.BOLD);
        var italic_button = new ToolButton.from_stock (Stock.ITALIC);
        var underline_button = new ToolButton.from_stock (Stock.UNDERLINE);
        
        var left_button = new ToolButton.from_stock (Stock.JUSTIFY_LEFT);
        left_button.clicked.connect (justify_left);
        var right_button = new ToolButton.from_stock (Stock.JUSTIFY_RIGHT);
        right_button.clicked.connect (justify_right);
        var center_button = new ToolButton.from_stock (Stock.JUSTIFY_CENTER);
        center_button.clicked.connect (justify_center);
        var fill_button = new ToolButton.from_stock (Stock.JUSTIFY_FILL);
        fill_button.clicked.connect (justify_fill);
        
        
        toolbar.add (new_button);
        toolbar.add (open_button);
        toolbar.add (save_button);
        toolbar.add (save_as_button);
        
        toolbar.add (separator);
        
        toolbar.add (bold_button);
        toolbar.add (italic_button);
        toolbar.add (underline_button);
        toolbar.add (left_button);
        toolbar.add (center_button);
        toolbar.add (right_button);
        toolbar.add (fill_button);
        
        toolbar.add (separator2);
        toolbar.add (menu_button);

        this.text_view = new TextView ();

        var scroll = new ScrolledWindow (null, null);
        scroll.set_policy (PolicyType.AUTOMATIC, PolicyType.AUTOMATIC);
        scroll.add (this.text_view);

        var vbox = new Box (Orientation.VERTICAL, 0);
        vbox.pack_start (toolbar, false, true, 0);
        vbox.pack_start (scroll, true, true, 0);
        add (vbox);
    }
    
    private void justify_left() {
        text_view.set_justification(Gtk.Justification.LEFT);
    }
    private void justify_right() {
        text_view.set_justification(Gtk.Justification.RIGHT);
    }
    private void justify_center() {
        text_view.set_justification(Gtk.Justification.CENTER);
    }
    private void justify_fill() {
        text_view.set_justification(Gtk.Justification.FILL);
    }
    
    private void on_open_clicked () {
        var file_chooser = new FileChooserDialog ("Open File", this,
                                      FileChooserAction.OPEN,
                                      Stock.CANCEL, ResponseType.CANCEL,
                                      Stock.OPEN, ResponseType.ACCEPT);
        if (file_chooser.run () == ResponseType.ACCEPT) {
            open_file (file_chooser.get_filename ());
        }
        file_chooser.destroy ();
    }
    
    private void on_save_as_clicked () {
        
        var file_chooser = new FileChooserDialog ("Save File", this,
                                      FileChooserAction.SAVE,
                                      Stock.CANCEL, ResponseType.CANCEL,
                                      Stock.SAVE, ResponseType.ACCEPT);
        if (file_chooser.run () == ResponseType.ACCEPT) {
            save_file (file_chooser.get_filename ());
        }
        file_chooser.destroy ();
    }
    
    private void on_save_clicked () {        
        save_file(f_name);
    }
    
    private void on_new_clicked() {
       messagebox_show ("Warning", "Are you sure you want to create a new document?");
       this.text_view.buffer.text = "";
       this.title = "New document - Draft";
    }
    
    private void messagebox_show(string title, string message) {
       var dialog = new Gtk.MessageDialog(null,Gtk.DialogFlags.MODAL, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, message);
   
    dialog.set_title(title);
    dialog.run();
    dialog.destroy();
    }

    private void open_file (string filename) {
        try {
            string text;
            FileUtils.get_contents (filename, out text);
            this.text_view.buffer.text = text;
            this.title = filename + " - Draft";
            f_name = filename;
        } catch (Error e) {
            stderr.printf ("Error: %s\n", e.message);
        }
    }

    private void save_file (string filename) {
        try {
            string text;
            text = this.text_view.buffer.text;
            FileUtils.set_contents (filename, text);
            this.title = filename + " - Draft";
        } catch (Error e) {
            stderr.printf ("Error: %s\n", e.message);
        }
    }
    
    public static int main (string[] args) {
        Gtk.init (ref args);

        var window = new TextFileViewer ();
        window.destroy.connect (Gtk.main_quit);
        window.show_all ();

        Gtk.main ();
        return 0;
    }
}
