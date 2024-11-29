import src.graphs as graphs, src.xml_writer as xml_writer, src.app as app
from src.log import log, logging
from math import ceil


import time



def main() :

    print('run')

    # log.setLevel(logging.DEBUG)


    #log.info(function)

    """
    
    
    graph.set_function(function)
    log.debug(graph.get_function())
    graph.calculate_interval(  -50,
                                50,
                                1,
                                True)
    print(graph.get_points())
    """

    window = app.Application()
    window.run()

    """
    Writer = xml_writer.XML_Writer(height, width, x_offset, y_offset, radius)
    Writer.Add_All_Points(graph.get_points(),radius)
    Writer.Final()
    """


main()
