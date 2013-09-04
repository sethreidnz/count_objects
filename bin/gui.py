import gtk
import thread

gtk.gdk.threads_init()
thread.start_new_thread(gtk.main, ())
