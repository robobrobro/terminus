#ifndef __TERMINUS_RESOURCES_RESOURCE_H__
#define __TERMINUS_RESOURCES_RESOURCE_H__

#include <memory>
#include <openssl/sha.h>

namespace terminus
{
    namespace resources
    {
        struct resource
        {
            uint64_t id;
            uint64_t payload_size;
            uint8_t payload_checksum[SHA512_DIGEST_LENGTH];
            uint8_t payload[0];
        };  // struct resource
    
        typedef std::shared_ptr<resource> resource_ptr;
    
        resource_ptr serialize(uint64_t id, uint8_t payload[], uint64_t payload_size);
        template<class T> std::shared_ptr<T> deserialize(const resource_ptr resource);
    }   // namespace resources
}   // namespace terminus

#endif  // __TERMINUS_RESOURCES_RESOURCE_H__
