#include <algorithm>
#include <cstring>
#include <terminus/resource.h>

namespace terminus
{
namespace resources
{
    resource_ptr serialize(uint64_t id, uint8_t payload[], uint64_t payload_size)
    {
        auto size = sizeof(uint8_t) * (sizeof(resource) + payload_size);
        auto res = std::make_shared<resource>();
        res->id = id;
        res->payload_size = payload_size;
        memcpy(res->payload, payload, payload_size);
        return res;
    }

    template<class T> std::shared_ptr<T> deserialize(const resource_ptr resource)
    {
    }
}   // namespace resources
}   // namespace terminus
