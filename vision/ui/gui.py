import PySimpleGUI as sg
import concurrent.futures 
import cv2

class gui:
    THREAD_EVENT = '-THREAD-'
    _general = None
    _executor = None
    
    def __init__(self,general):
        self._general = general
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
        #sg.Window(title="Hello World", layout=[[]], margins=(100, 50)).read()
        sg.theme('DarkAmber')   # Add a touch of color
        items = ["item 3"]
        list_tool = [   [sg.Text("tool list")],
                        [sg.Listbox(values=items, size=(20, 6), key="items_listbox")]
                    ]
        # All the stuff inside your window.
        layout = [  
                    [sg.Text('Some text on Row 1')],
                    [sg.Text('Enter something on Row 2'), sg.InputText()],
                    [sg.Col(list_tool),sg.Graph((200,200),(0,200), (200,0), key='-GRAPH-', enable_events=True, drag_submits=True)],
                    [sg.Button('Detect'),sg.Button('Update'),sg.Button('Ok'), sg.Button('Cancel')] 
                 ]

        # Create the Window
        window = sg.Window('Window Title', layout, resizable=True).Finalize()
        window.Maximize()
        
        #window['items_listbox'].expend(expand_y=True)
        window['-GRAPH-'].expand(expand_x=True, expand_y=True, expand_row=True)
        self._a_id = None
        
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()
            print(event,values)
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
            if event == 'Detect':
                task = self._executor.submit(self.detect,window)
                task.add_done_callback(self.done_callback)
            if event == 'Ok':
                print('You entered ', values[0])
            if event == 'Update':
                self.update(window)
            if event == self.THREAD_EVENT:
                print("hi")
                print(values[self.THREAD_EVENT])
                self.update(window)
                items = ["item 1"]

        window.close()
    
    def get_coord(self,ori_area,coord,target_area):
        #print(ori_area)
        #print(coord)
        #print(target_area)
        ori_area = list(ori_area)
        coord = list(coord)
        target_area = list(target_area)
        #print(ori_area)
        #print(coord)
        #print(target_area)
        coord[0] = int((target_area[0]/ori_area[0])*coord[0])
        coord[1] = int((target_area[1]/ori_area[1])*coord[1])
        #print(coord)
        return coord
    
    def update(self,window):
        graph_elem = window['-GRAPH-'] 
        size_of_graph = graph_elem.get_size()   

        #print('Width:', size_of_graph[0], 'pixels')
        #print('Height:', size_of_graph[1], 'pixels')  
        
        img = self._general._flow._images["Camera1"]
        
        area_img = img.shape[:2]
        area_img = area_img[::-1]
        area_img = (img.shape[1],img.shape[0])
        resized = cv2.resize(img, size_of_graph)
        
        imgbytes = cv2.imencode('.png',resized)[1].tobytes()                
        if self._a_id:
            graph_elem.delete_figure(self._a_id)             # delete previous image
        self._a_id = graph_elem.draw_image(data=imgbytes, location=(0,0))    # draw new image
        graph_elem.TKCanvas.tag_lower(self._a_id)  
        
        for item in self._general._flow._flowing[self._general._flow._name]:
            print(item['obj']._output)
            if item['obj'].type == "template_match":
                start_point = self.get_coord(area_img,(item['obj']._output['x'],item['obj']._output['y']),size_of_graph)
                end_point = self.get_coord(area_img,(item['obj']._output['x2'],item['obj']._output['y2']),size_of_graph)
                
                graph_elem.draw_rectangle(start_point, end_point,fill_color='green', line_color='red')
                print(item['obj']._output)
    
    def detect(self,window):
        self._general.detect()
        
        window.write_event_value(self.THREAD_EVENT, ("a","b"))
        return "ok"
        
        
    def done_callback(self,future_obj):
        if future_obj.cancelled():
            print('Future object was cancelled')
        elif future_obj.done():
            error = future_obj.exception()
            if error:
                print('Future threw exception')
            else:
                result = future_obj.result()
                print('Got result', result)
