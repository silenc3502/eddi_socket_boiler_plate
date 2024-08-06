from acceptor.service.socket_accept_service_impl import SocketAcceptServiceImpl
from custom_protocol.entity.default_protocol import DefaultProtocolNumber
from custom_protocol.service.custom_protocol_service_impl import CustomProtocolServiceImpl
from dice.service.dice_service_impl import DiceServiceImpl
from ipc_queue.repository.ipc_queue_repository_impl import IPCQueueRepositoryImpl
from ipc_queue.service.ipc_queue_service_impl import IPCQueueServiceImpl
from receiver.service.receiver_service_impl import ReceiverServiceImpl
from server_socket.service.server_socket_service_impl import ServerSocketServiceImpl
from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl
from transmitter.service.transmitter_service_impl import TransmitterServiceImpl


class DomainInitializer:
    @staticmethod
    def initDiceDomain():
        DiceServiceImpl.getInstance()

    @staticmethod
    def initCustomProtocolDomain():
        customProtocolService = CustomProtocolServiceImpl.getInstance()
        diceService = DiceServiceImpl.getInstance()

        # 디폴트 프로토콜 등록을 여기서 했음
        customProtocolService.registerCustomProtocol(
            DefaultProtocolNumber.DICE_ROLL_JUST_FOR_TEST,
            diceService.rollDice
        )

        customProtocolService.registerCustomProtocol(
            DefaultProtocolNumber.DICE_LIST_JUST_FOR_TEST,
            diceService.diceList
        )

    @staticmethod
    def initIPCQueueDomain():
        ipcQueueService = IPCQueueServiceImpl.getInstance()
        ipcQueueService.createDefaultIPCQueue()

    @staticmethod
    def initTaskWorkerDomain():
        TaskWorkerServiceImpl.getInstance()

    @staticmethod
    def initServerSocketDomain():
        ServerSocketServiceImpl.getInstance()

    @staticmethod
    def initSocketAcceptDomain():
        ipcQueueRepository = IPCQueueRepositoryImpl.getInstance()
        ipcAcceptorReceiverChannel = ipcQueueRepository.getIPCAcceptorReceiverChannel()
        ipcAcceptorTransmitterChannel = ipcQueueRepository.getIPCAcceptorTransmitterChannel()

        socketAcceptService = SocketAcceptServiceImpl.getInstance()
        socketAcceptService.requestToInjectAcceptorReceiverChannel(ipcAcceptorReceiverChannel)
        socketAcceptService.requestToInjectAcceptorTransmitterChannel(ipcAcceptorTransmitterChannel)

    @staticmethod
    def initReceiverDomain():
        ipcQueueRepository = IPCQueueRepositoryImpl.getInstance()
        ipcAcceptorReceiverChannel = ipcQueueRepository.getIPCAcceptorReceiverChannel()

        receiverService = ReceiverServiceImpl.getInstance()
        receiverService.requestToInjectAcceptorReceiverChannel(ipcAcceptorReceiverChannel)

    @staticmethod
    def initTransmitterDomain():
        ipcQueueRepository = IPCQueueRepositoryImpl.getInstance()
        ipcAcceptorTransmitterChannel = ipcQueueRepository.getIPCAcceptorTransmitterChannel()

        transmitterService = TransmitterServiceImpl.getInstance()
        transmitterService.requestToInjectAcceptorTransmitterChannel(ipcAcceptorTransmitterChannel)

    @staticmethod
    def initEachDomain():
        DomainInitializer.initDiceDomain()
        DomainInitializer.initCustomProtocolDomain()

        DomainInitializer.initIPCQueueDomain()
        DomainInitializer.initTaskWorkerDomain()
        DomainInitializer.initServerSocketDomain()
        DomainInitializer.initSocketAcceptDomain()
        DomainInitializer.initReceiverDomain()
        DomainInitializer.initTransmitterDomain()

