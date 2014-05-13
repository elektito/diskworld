import logging

class IntegrationHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            # if this is an integration record
            if hasattr(record, 'f0'):
                l1 = '+-- Integration {}-------------------------------------+'
                l2 = '| non-contact forces: {}'
                l3 = '| contact forces: {}'
                l4 = '| new velocities: {}'
                l5 = '| new positions: {}'
                l6 = '+----------------------------------------------------------------+'

                l1 = l1.format('[collision] '
                               if len(record.c1) > 0 and any(len(r) > 0 for r in record.c1)
                               else '------------')
                l2 = l2.format(record.f1)
                l3 = l3.format([f2 - f1 for f1, f2 in zip(record.f1, record.f2)])
                l4 = l4.format(record.v2)
                l5 = l5.format(record.x1)

                msg = '\n'.join([l1, l2, l3, l4, l5, l6]) + '\n'
                self.stream.write(msg)
                self.flush()
        except KeyboardInterrupt, SystemExit:
            raise
        except:
            self.handleError(record)
