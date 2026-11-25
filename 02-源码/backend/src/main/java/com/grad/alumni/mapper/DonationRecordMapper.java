package com.grad.alumni.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.entity.DonationRecord;
import org.apache.ibatis.annotations.Mapper;

/** DonationRecord 数据访问 */
@Mapper
public interface DonationRecordMapper extends BaseMapper<DonationRecord> {
}
