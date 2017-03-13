class FileSystem:
    def __init__(self, size):
        self.size = size
        self.available_size = size - 1
        self.root = Directory('/')

    @staticmethod
    def __get_paths(path):
        parent_paths = []
        cur_node = ''
        for node in path[1:].split('/')[:-1]:
            cur_node += '/' + node
            parent_paths.append(cur_node)
        return parent_paths

    @staticmethod
    def __split(path):
        previous_node = [node for node in path.rpartition('/')
                         if node != '']
        return previous_node[0], previous_node[-1]

    @staticmethod
    def __find_node(name, directory):
        found = None
        if type(directory) is Directory:
            found = [node for node in directory.nodes
                     if name == node.name]
        if found:
            return found[0]
        else:
            return None

    def get_node(self, path):
        if not path.startswith('/'):
            raise NodeDoesNotExistError
        current = self.root
        split_path = [node for node in path.split('/') if node != '']
        for node in split_path:
            found = self.__find_node(node, current)
            if found:
                current = found
            else:
                raise NodeDoesNotExistError
        return current

    def create(self, path, directory=False, content=''):
        try:
            head, tail = self.__split(path)
            parent = self.get_node(head)
            if self.__find_node(tail, parent):
                raise DestinationNodeExistsError
            elif type(parent) is File:
                raise NodeDoesNotExistError
            elif (len(content) + 1 > self.available_size
                  or self.available_size < 1):
                raise NotEnoughSpaceError
        except NodeDoesNotExistError:
            raise DestinationNodeDoesNotExistError
        else:
            if directory:
                new_directory = Directory(tail)
                parent.nodes.append(new_directory)
                parent.directories.append(new_directory)
                self.available_size -= 1
                self.root.size += new_directory.size
                for parent_path in self.__get_paths(path):
                    self.get_node(parent_path).size += new_directory.size
            else:
                new_file = File(tail, content)
                parent.nodes.append(new_file)
                parent.files.append(new_file)
                self.available_size -= new_file.size
                self.root.size += new_file.size
                for parent_path in self.__get_paths(path):
                    self.get_node(parent_path).size += new_file.size

    def remove(self, path, directory=False, force=True):
        target = self.get_node(path)
        head, tail = self.__split(path)
        if type(target) is Directory and not directory:
            raise NonExplicitDirectoryDeletionError
        elif (type(target) is Directory and directory
              and target.nodes and not force):
            raise NonEmptyDirectoryDeletionError
        parent = self.get_node(head)
        found = self.__find_node(target.name, parent)
        self.available_size += found.size
        self.root.size -= target.size
        for parent_path in self.__get_paths(path):
            self.get_node(parent_path).size -= target.size
        del parent.nodes[parent.nodes.index(found)]
        if target.pointed_by:
            for link in target.pointed_by:
                self.get_node(link).link_path = None
        if directory:
            del parent.directories[parent.directories.index(found)]
        else:
            del parent.files[parent.files.index(found)]

    def move(self, source, destination):
        try:
            source_node = self.get_node(source)
        except NodeDoesNotExistError:
            raise SourceNodeDoesNotExistError
        try:
            destination_node = self.get_node(destination)
        except NodeDoesNotExistError:
            raise DestinationNodeDoesNotExistError
        if type(destination_node) is not Directory:
            raise DestinationNotADirectoryError
        found = self.__find_node(source_node.name, destination_node)
        if found:
            raise DestinationNodeExistsError
        head, tail = self.__split(source)
        parent = self.get_node(head)
        destination_node.nodes.append(source_node)
        del parent.nodes[parent.nodes.index(source_node)]
        if type(source_node) is File:
            destination_node.files.append(source_node)
            del parent.files[parent.files.index(source_node)]
        else:
            destination_node.directories.append(source_node)
            del parent.directories[parent.directories.index(source_node)]
        for parents in self.__get_paths(source):
            self.get_node(parents).size -= source_node.size
        for parents in self.__get_paths(destination):
            self.get_node(parents).size += source_node.size
        destination_node.size += source_node.size

    def mount(self, file_system, path):
        try:
            target = self.get_node(path)
            if type(target) is File:
                raise MountPointNotADirectoryError
            elif target.nodes:
                raise MountPointNotEmptyError
        except NodeDoesNotExistError:
            raise MountPointDoesNotExistError
        else:
            mounted = file_system.get_node('/')
            head, tail = self.__split(path)
            parent = self.get_node(head)
            del parent.nodes[parent.nodes.index(target)]
            del parent.directories[parent.directories.index(target)]
            parent.nodes.append(mounted)
            parent.directories.append(mounted)
            mounted.name = tail
            mounted.is_mount = True

    def unmount(self, path):
        target = self.get_node(path)
        if not target.is_mount:
            raise NotAMountpointError
        self.remove(path, directory=True)
        self.create(path, directory=True)

    def link(self, source, destination, symbolic=True):
        try:
            target = self.get_node(source)
            if type(target) is Directory and not symbolic:
                raise DirectoryHardLinkError
        except NodeDoesNotExistError:
            if symbolic:
                raise NodeDoesNotExistError
            else:
                raise SourceNodeDoesNotExistError
        else:
            head, tail = self.__split(destination)
            parent = self.get_node(head)
            found = self.__find_node(tail, parent)
            if found:
                if symbolic:
                    found.link_path = target
            else:
                if symbolic:
                    if type(target) is File:
                        link = File(tail, '')
                        del link.content
                        parent.files.append(link)
                    else:
                        link = Directory(tail)
                        del link.nodes
                        del link.files
                        del link.directories
                        parent.directories.append(link)
                    link.link_path = target
                    link.symbolic = True
                else:
                    link = File(tail, target.content)
                    link.hard_link = target
                parent.nodes.append(link)
                self.available_size -= 1
                self.root.size += 1
                for parent in self.__get_paths(destination):
                    self.get_node(parent).size += 1
            if symbolic:
                target.pointed_by.append(destination)
            else:
                target.hard_links.append(link)


class File:
    def __init__(self, name, content):
        self.name = name
        self.is_directory = False
        self.symbolic = False
        self.hard_link = False
        self.link_path = None
        self.pointed_by = []
        self.hard_links = []
        self.content = content
        self.size = len(self.content) + 1

    def append(self, text):
        if self.hard_link:
            self.hard_link.content += text
        elif self.hard_links:
            for hard_link in self.hard_links:
                hard_link.content += text
        self.content += text
        self.size += len(text)

    def truncate(self, text):
        if self.hard_link:
            self.hard_link.content = text
        elif self.hard_links:
            for hard_link in self.hard_links:
                hard_link.content = text
        self.content = text
        self.size = len(text)

    def __getattr__(self, item):
        if self.link_path and hasattr(self.link_path, item):
            return self.link_path.__dict__[item]
        else:
            raise LinkPathError


class Directory:
    def __init__(self, name):
        self.name = name
        self.size = 1
        self.is_directory = True
        self.is_mount = False
        self.symbolic = False
        self.link_path = None
        self.pointed_by = []
        self.directories = []
        self.files = []
        self.nodes = []

    def __getattr__(self, item):
        if self.link_path and hasattr(self.link_path, item):
            return self.link_path.__dict__[item]
        else:
            raise LinkPathError


class FileSystemError(Exception):
    pass


class FileSystemMountError(FileSystemError):
    pass


class MountPointDoesNotExistError(FileSystemMountError):
    pass


class MountPointNotADirectoryError(FileSystemMountError):
    pass


class MountPointNotEmptyError(FileSystemMountError):
    pass


class NodeDoesNotExistError(FileSystemError):
    pass


class SourceNodeDoesNotExistError(NodeDoesNotExistError):
    pass


class DestinationNodeDoesNotExistError(NodeDoesNotExistError):
    pass


class NotAMountpointError(FileSystemMountError):
    pass


class NotEnoughSpaceError(FileSystemError):
    pass


class DestinationNodeExistsError(FileSystemError):
    pass


class NonExplicitDirectoryDeletionError(FileSystemError):
    pass


class NonEmptyDirectoryDeletionError(FileSystemError):
    pass


class DestinationNotADirectoryError(FileSystemError):
    pass


class DirectoryHardLinkError(FileSystemError):
    pass


class LinkPathError(FileSystemError):
    pass
