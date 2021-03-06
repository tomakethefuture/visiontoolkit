import PySimpleGUI as sg
from vision.image.source import source
import cv2



def main(general):
    sg.theme('Dark Blue 3')
    
    col_list = [[sg.Button('Detect')],
                [sg.Text("tool list")],
                [sg.Listbox(values=["Camera1"], size=(20, 8), enable_events=True,change_submits= True, key="-LIST-")]
                ]
    
    layout = [[sg.Col(col_list),
                sg.Graph(
                canvas_size=(400, 400),
                graph_bottom_left=(0, 800),
                graph_top_right=(800, 0),
                key="-GRAPH-",
                enable_events=True,
                background_color='lightblue',
                drag_submits=True)]]
                
    # _config = config.get_config(default.FILE_NAME_CONFIG_VISION,structure.CONFIG_VISION)
    # self._source = source()
    # self._source.load(_config.source)
    
    # self._source.get()
    window = sg.Window('FMC General 4.0.0-dev', layout, resizable=True).Finalize()
    window['-GRAPH-'].expand(expand_x=True, expand_y=True, expand_row=True)
    #window['-LIST-'].expand(expand_x=True, expand_y=True, expand_row=True) #notworking
    
    _id_image = None
    graph_elem = window['-GRAPH-']
    
    list_tools = []
    for item in general._source._sources.keys():
        print(item)
        list_tools.append(item)
    for tool in general._flow._current[general._flow._name]:
        print(tool)
        list_tools.append(tool['name'])
    window['-LIST-'].Update(list_tools) 
    
    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
               
        elif event in ( 'Detect','-LIST-'):
            if event == 'Detect':
                general.detect()   
              
            print(values['-LIST-'])
            print(general._flow._current)
            print(general._source._sources)
            #window.Element('-LIST-').Update(set_to_index=10, scroll_to_index=7)
            
            displayed = False
            size_of_graph = graph_elem.get_size()
            
            if len(values['-LIST-'])==1:
                for item in general._source._sources.keys():
                    print(item)
                    if item == values['-LIST-'][0]:
                        displayed = True
                        
                        img = general._flow._images[item]
                        if img is not None:
                            resized = cv2.resize(img, size_of_graph)
                            if _id_image:
                                graph_elem.delete_figure(_id_image)
                            imgbytes = cv2.imencode('.png',resized)[1].tobytes() 
                            _id_image = graph_elem.draw_image(data=imgbytes, location=(0,0)) 
                    #list_tools.append(item)
            if not displayed:
                for tool in general._flow._current[general._flow._name]:
                    if tool['obj']._output.image is not None and displayed == False: 
                     #tool['obj'].type == "contour_match" ):#and tool['obj']._name=="":
                        if hasattr(tool['obj']._output, 'new_attrib'):
                            # obj.attr_name exists.
                            print(tool['obj']._output.new_attrib)
                     
                        img = tool['obj']._output.image
                        if img is not None:
                            resized = cv2.resize(img, size_of_graph)
                            if _id_image:
                                graph_elem.delete_figure(_id_image)
                            imgbytes = cv2.imencode('.png',resized)[1].tobytes() 
                            _id_image = graph_elem.draw_image(data=imgbytes, location=(0,0)) 
                            displayed = True
                    elif tool['obj']._output.x is not None and displayed == False:
                        img = general._flow._images[tool['obj']._config['source']]
                        if img is not None:
                            resized = cv2.resize(img, size_of_graph)
                            print(size_of_graph)
                            if _id_image:
                                graph_elem.delete_figure(_id_image)
                            imgbytes = cv2.imencode('.png',resized)[1].tobytes() 
                            _id_image = graph_elem.draw_image(data=imgbytes, location=(0,0))
                            displayed = True
    window.close()        