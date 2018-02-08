from lxml import etree
import yaml

def format_addr(addr):
  return "0x{:08X}".format(addr)

def add_nodes_to_root(root_node, doc):
  print doc
  for node in doc.get('nodes', []):
    node_id = node.get('id', 'ID')
    node_addr = format_addr(node.get('address', 0))
    node_descr = node.get('description', node_id)
    add_nodes_to_root(etree.SubElement(root_node, "node", id=node_id, address=node_addr, description=node_descr), node)

doc = yaml.load(file('xadc.yml'))

root = etree.Element('node', id="TOP")
add_nodes_to_root(root, doc)

print etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="utf-8")
